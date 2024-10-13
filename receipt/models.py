from django.db import models
from mindee import Client, PredictResponse, product
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MINDEE_API_KEY = os.getenv('MINDEE_API_KEY_ENV')
mindee_client = Client(api_key=MINDEE_API_KEY)

class Receipt(models.Model):
    image = models.ImageField(upload_to='image_receipts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def extract_data(self):
        # Logica de extração dos dados usando Mindee
        try:
            
            # Carregar a imagem e processar com Mindee
            input_doc = mindee_client.source_from_path(self.image.path)
            result: PredictResponse = mindee_client.parse(product.ReceiptV5, input_doc)
            
            # Retorna os dados extraídos como dicionário
            print('Dados extraidos com sucesso')
            
            return {
                'extracted_locale': result.document.inference.prediction.locale.value,
                'extracted_shop_name': result.document.inference.prediction.supplier_name.value,
                'extracted_category': result.document.inference.prediction.category.value,
                'extracted_date': result.document.inference.prediction.date.value,
                'extracted_total_tax': result.document.inference.prediction.total_tax.value,
                'extracted_total_amount': result.document.inference.prediction.total_amount.value,
                'line_items': [{
                    'description': line_item.description,
                    'quantity': line_item.quantity,
                    'unit_price': line_item.unit_price,
                    'total_amount': line_item.total_amount,
                } for line_item in result.document.inference.prediction.line_items]
            }
                    
        except Exception as e:
            print(f'Erro ao Extrair dados: {e}')
            return None

    def __str__(self):
        return f'Receipt {self.id} - {self.uploaded_at}'

# Coletando dados para o servidor
class ExtractingResults(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='extraction_results', null=True, blank=True)
    extracted_locale = models.CharField(max_length=10)
    extracted_shop_name = models.CharField(max_length=100, null=True, blank=True)
    extracted_category = models.CharField(max_length=50, null=True, blank=True)
    extracted_date = models.DateField(null=True, blank=True)
    extracted_total_tax = models.FloatField(null=True, blank=True)
    extracted_total_amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.extracted_total_amount = round(self.extracted_total_amount, 2)
        super(ExtractingResults, self).save(*args, **kwargs)
    

    @classmethod
    def total_amount_per_month(cls):
        # Agrega os valores por mês
        results = cls.objects.annotate(month=TruncMonth('extracted_date')) \
            .values('month') \
            .annotate(total_amount=Sum('extracted_total_amount')) \
            .order_by('month')
        
        return list(results)
    
    @classmethod
    def total_amount_per_year(cls):
        # Agrega os valores por ano
        extracted_total_amount = round(extracted_total_amount, 2)
        results = cls.objects.annotate(year=TruncYear('extracted_date')) \
            .values('year') \
            .annotate(total_amount=Sum('extracted_total_amount')) \
            .order_by('year')
        
        return list(results)
    
    @classmethod
    def total_amount_per_category_per_month(cls, year):
        # Agrega os valores por mês, ano e categoria
        results = cls.objects.annotate(month=TruncMonth('extracted_date')) \
        .values('month', 'extracted_category').annotate(total_amount=Sum('extracted_total_amount')) \
        .order_by('month', 'extracted_category')  # Ordenando por mês e categoria
       
        return list(results)



class ExtractedLineItem(models.Model):
    extraction = models.ForeignKey(ExtractingResults, on_delete=models.CASCADE, related_name='line_items')
    description = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=1,null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'LineItem {self.description} - {self.total_amount}'
