from django.contrib import admin
from .models import Receipt, ExtractingResults, ExtractedLineItem

class ExtractedLineItemInline(admin.TabularInline):
    model = ExtractedLineItem
    extra = 1  # Quantidade de formulários em branco para adicionar itens

class ExtractingResultsAdmin(admin.ModelAdmin):
    list_display = ('extracted_locale', 'extracted_shop_name', 'extracted_category', 'extracted_date', 'extracted_total_tax', 'extracted_total_amount', 'created_at')
    inlines = [ExtractedLineItemInline]

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('image', 'uploaded_at')
    search_fields = ['image']

admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(ExtractingResults, ExtractingResultsAdmin)



