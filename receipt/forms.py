from django import forms
from .models import Receipt, ExtractingResults, ExtractedLineItem
from django.contrib.admin.options import InlineModelAdmin

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Verifica se a imagem já existe no banco de dados
        if Receipt.objects.filter(image=image.name).exists():
            raise forms.ValidationError("An image with the same name has already been uploaded.")
        return image


class ExtractingResultsForm(forms.ModelForm):
    class Meta:
        model = ExtractingResults
        fields = ['extracted_locale', 'extracted_shop_name', 'extracted_category', 'extracted_date', 'extracted_total_tax', 'extracted_total_amount']
        widgets = {
            'extracted_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExtractedLineItemForm(forms.ModelForm):
    class Meta:
        model = ExtractedLineItem
        fields = ['description', 'quantity', 'unit_price', 'total_amount']


class EditExtractingResultsForm(forms.ModelForm):
    class Meta:
        model = ExtractingResults
        fields = ['extracted_locale', 'extracted_shop_name', 'extracted_category', 'extracted_date', 'extracted_total_tax', 'extracted_total_amount']


class EditExtratedLineItemForm(forms.ModelForm):
    class Meta:
        model = ExtractedLineItem
        fields = ['description', 'quantity', 'unit_price', 'total_amount']

