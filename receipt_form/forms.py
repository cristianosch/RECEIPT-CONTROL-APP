from django import forms
from receipt.models import Receipt, ExtractingResults, ExtractedLineItem
from django.forms import inlineformset_factory


class AddReceiptForm(forms.ModelForm):
    class Meta:
        model = ExtractingResults
        fields = [                                   
            'extracted_locale', 
            'extracted_shop_name', 
            'extracted_category', 
            'extracted_date', 
            'extracted_total_tax', 
            'extracted_total_amount'
            ]
        widgets = {            
            'extracted_date': forms.DateInput(attrs={'type': 'date'}),
            'extracted_locale': forms.TextInput(attrs={'placeholder': 'Ex. PT', 'max_length': 100}),
            'extracted_total_tax': forms.NumberInput(attrs={'max': 1000}),
            'extracted_total_amount': forms.NumberInput(attrs={'max': 10000}),
        }


class AddItemForm(forms.ModelForm):
    class Meta:
        model = ExtractedLineItem
        fields = [
            'description', 
            'quantity', 
            'unit_price', 
            'total_amount'
            ]

LineItemFormSet = forms.inlineformset_factory(ExtractingResults, ExtractedLineItem, form=AddItemForm, extra=1, can_delete=True) 

