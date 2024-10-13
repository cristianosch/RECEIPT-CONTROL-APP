from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import AddReceiptForm, LineItemFormSet
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from receipt.models import Receipt


class FormAddReceiptView(View):
    def get(self, request):
        form = AddReceiptForm()
        line_item_formset = LineItemFormSet()
        return render(request, 'receipt_form/add_manual_receipt.html', {
            'form': form,
            'line_item_formset': line_item_formset,
        })
    def post(self, request):
        form = AddReceiptForm(request.POST)
        line_item_formset = LineItemFormSet(request.POST)

        if form.is_valid() and line_item_formset.is_valid():  
            manual_receipt = Receipt.objects.create()
            extraction = form.save(commit=False)
            extraction.receipt = manual_receipt      
            extraction.save()

            # Associa a instância de extração ao formset de itens de linha
            for line_item_form in line_item_formset:
                line_item = line_item_form.save(commit=False)
                line_item.extraction = extraction
                line_item.save()

            messages.success(request, 'Receipt successfully saved')
            return redirect('add_manual_receipt')
        else:
            messages.error(request, 'Falided to save the receipt. Please check the form.')
        
        return render(request, 'receipt_form/add_manual_receipt.html', {
            'form': form,
            'line_item_formset':line_item_formset,
        })





