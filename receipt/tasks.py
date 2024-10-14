from celery import shared_task
from time import sleep
from receipt.models import Receipt, ExtractingResults, ExtractedLineItem
import time


@shared_task
def process_image_extraction(receipt_id):    
    # Simula o processamento da extração da imagem
    receipt = Receipt.objects.get(id=receipt_id)

    # Simular uma tarefa demorada
    time.sleep(2)  # Substitua isso pelo código real de extração de imagem

    extracted_data = receipt.extract_data()
    if extracted_data:
        # Processa os dados extraídos
        extraction = ExtractingResults.objects.create(
            receipt=receipt,
            extracted_locale=extracted_data.get('extracted_locale'),
            extracted_shop_name=extracted_data.get('extracted_shop_name'),
            extracted_category=extracted_data.get('extracted_category'),
            extracted_date=extracted_data.get('extracted_date'),
            extracted_total_tax=extracted_data.get('extracted_total_tax'),
            extracted_total_amount=extracted_data.get('extracted_total_amount')
        )

        for line_item_data in extracted_data.get('line_items', []):
            ExtractedLineItem.objects.create(
                extraction=extraction,
                description=line_item_data.get('description'),
                quantity=line_item_data.get('quantity'),
                unit_price=line_item_data.get('unit_price'),
                total_amount=line_item_data.get('total_amount')
            )
        return "Extraction completed"
    return "Extraction failed"
