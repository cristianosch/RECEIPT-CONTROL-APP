from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Receipt, ExtractingResults, ExtractedLineItem
from .forms import ReceiptForm, ExtractingResultsForm, ExtractedLineItemForm, EditExtractingResultsForm, EditExtratedLineItemForm
from django.contrib.messages import constants
from django.contrib import messages
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count, Q
from calendar import month_name
from django.utils.dateformat import DateFormat
from django.db.models import Sum
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from datetime import datetime, timedelta
from .utils import plot_pie_chart_plotly
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .tasks import process_image_extraction


def get_last_three_months():
    # Obtém a data atual
    current_date = datetime.now()
    
    # Calcula a data que corresponde ao início do período de três meses atrás
    three_months_ago = current_date - timedelta(days=90)

    # Filtra os resultados para os últimos três meses
    last_three_months_totals = ExtractingResults.objects.annotate(month=TruncMonth('extracted_date')) \
                                                        .filter(extracted_date__gte=three_months_ago) \
                                                        .values('month') \
                                                        .annotate(total_amount=Sum('extracted_total_amount')) \
                                                        .order_by('month')
    labels = [item['month'].strftime('%B %Y') for item in last_three_months_totals]
    data = [item['total_amount'] for item in last_three_months_totals]

    # Passar os dados para o template
    return {
        'labels': labels,
        'data': data,
    }
    

def get_current_month_total():
    # Obtém o mês e ano atuais
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Filtra os resultados pelo mês e ano atuais e agrupa por mês
    current_month_total = ExtractingResults.objects.annotate(month=TruncMonth('extracted_date')) \
                                                   .filter(extracted_date__year=current_year, extracted_date__month=current_month) \
                                                   .aggregate(total_amount=Sum('extracted_total_amount'))

    return current_month_total['total_amount'] if current_month_total['total_amount'] else 0



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'receipts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtendo resultado dos ultimos 3 meses
        last_three_months = get_last_three_months()

        # Obtendo resultado total do mês atual
        current_month_total = get_current_month_total()
        
        # Obtendo resultado total do ano
        year_totals = ExtractingResults.objects.annotate(year=TruncYear('extracted_date')) \
                                              .values('year') \
                                              .annotate(total_amount=Sum('extracted_total_amount')) \
                                              .order_by('year')
        
        # Convertendo o QuerySet em uma lista de Dicionarios        
        year_totals_list = list(year_totals)

        # Obter o ano a partir dos parâmetros da query string, ou usar o ano atual por padrão
        year = self.request.GET.get('year', datetime.now().year)
        try:
            year = int(year)
        except ValueError:
            year = datetime.now().year

        # Obtendo os totais mensais para o gráfico do ano solicitado
        monthly_totals = ExtractingResults.objects.filter(extracted_date__year=year) \
                                                  .annotate(month=TruncMonth('extracted_date')) \
                                                  .values('month') \
                                                  .annotate(total_amount=Sum('extracted_total_amount')) \
                                                  .order_by('month')

        monthly_labels = [entry['month'].strftime('%B') for entry in monthly_totals]
        monthly_data = [entry['total_amount'] for entry in monthly_totals]

        # Obtendo Valores totais por categoria        
        monthly_extracted_category_totals = ExtractingResults.total_amount_per_category_per_month
        
        context['year_totals_list'] = year_totals_list
        context['current_month_total'] = current_month_total
        context['last_three_months'] = last_three_months
        context['current_year'] = datetime.now().year
        context['previous_year'] = year - 1
        context['monthly_extracted_category_totals'] = monthly_extracted_category_totals
        

        # Dados para o gráfico do ano solicitado
        context['monthly_chart_data'] = {
            'labels': monthly_labels,
            'data': monthly_data,
        }

        # Dados para o gráfico dos últimos 3 meses
        context['last_three_months_chart_data'] = last_three_months

        return context           
    

class CategoryTable(LoginRequiredMixin, TemplateView):
    template_name = 'receipts/category_information.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get('year', datetime.now().year)
        try:
            year = int(year)
        except ValueError:
            year = datetime.now().year

        monthly_extracted_category_totals = ExtractingResults.total_amount_per_category_per_month(year)

        monthly_data = {}
        for result in monthly_extracted_category_totals:
            month = result['month'].strftime('%B %Y')
            if month not in monthly_data:
                monthly_data[month] = {
                    'labels': [],
                    'data': [],
                }
            monthly_data[month]['labels'].append(result['extracted_category'])
            monthly_data[month]['data'].append(result['total_amount'])
        
        # Ordenar os meses de forma decrescente
        sorted_monthly_data = dict(sorted(monthly_data.items(), reverse=True))

        # Adicionar os dados processados ao contexto
        context['monthly_chart_images'] = {}
        for month, data in sorted_monthly_data.items():
            chart_img = plot_pie_chart_plotly(data['data'], data['labels'])
            context['monthly_chart_images'][month] = mark_safe(f"data:image/png;base64,{chart_img}")

        context['monthly_extracted_category_totals'] = monthly_extracted_category_totals
        return context
    
    
@login_required
def add_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save()

            # Chama a tarefa Celery para processar a extração da imagem
            process_image_extraction.delay(receipt.id)

            messages.success(request, 'Receipt saved successfully! Extraction is processing in the background.')
            return redirect('receipts')

        else:
            form.add_error(None, "Erro ao processar o formulário.")
    
    else:
        form = ReceiptForm()

    return render(request, 'receipts/add-receipt.html', {'form': form})

 
@login_required
def receipts_by_month(request, year, month):
    # Obtenha os resultados da extração filtrados pela data extraída (extracted_date)
    extraction_results = ExtractingResults.objects.filter(extracted_date__year=year, extracted_date__month=month)
    
    # Prepara os dados para o template
    receipts_data = []
    for result in extraction_results:
        receipt = result.receipt
        extracted_items = result.line_items.all()

        receipt_data = {
            'receipt': receipt,
            'extraction_results': result,
            'extracted_items': extracted_items
        }
        receipts_data.append(receipt_data)

    # Convertendo o número do mês para o nome completo
    month_name = DateFormat(extraction_results.first().extracted_date).format('F') if extraction_results else None

    # Passa o contexto para o template
    context = {
        'month': month_name or month,  # Exibe o nome do mês ou o número caso não tenha extrações
        'year': year,
        'receipts_data': receipts_data,
    }

    return render(request, 'receipts/receipts_by_month.html', context)


@login_required
def edit_receipt(request, pk):
    # Obtenha o ExtractingResults usando o pk
    extracting_results = get_object_or_404(ExtractingResults, id=pk)
    
    # Criar um formset para editar múltiplos itens de linha
    LineItemFormSet = inlineformset_factory(
        ExtractingResults, 
        ExtractedLineItem, 
        form=EditExtratedLineItemForm, 
        extra=0,  
        can_delete=True  
    )

    # Instanciar o form para EditExtractingResults
    form = EditExtractingResultsForm(instance=extracting_results)
    formset = LineItemFormSet(instance=extracting_results)

    if request.method == 'POST':
        # Processar o formulário do recibo
        form = EditExtractingResultsForm(request.POST, instance=extracting_results)
        formset = LineItemFormSet(request.POST, instance=extracting_results)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            receipt_year = extracting_results.extracted_date.year
            receipt_month = extracting_results.extracted_date.month

            messages.success(request, "Receipt and line items edited successfully")
            return redirect('receipts_by_month', year=receipt_year, month=receipt_month)
        else:
            messages.error(request, "There was an error editing the receipt or items.")

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'receipts/edit_receipt.html', context)

    
@login_required
def receipts(request):
    items_per_page = request.GET.get('items_per_page', 5)  # Pega o valor da URL ou usa o padrão de 10
    # Obter todos os meses e anos com base na data extraída do recibo
    receipts = Receipt.objects.filter(extraction_results__extracted_date__isnull=False) \
        .annotate(month=TruncMonth('extraction_results__extracted_date')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('-month')

    # Criar uma lista de meses e anos
    months = [{'year': receipt['month'].year, 'month': receipt['month'].month, 'count': receipt['count']} for receipt in receipts]

    # Configurar o paginator
    paginator = Paginator(receipts, items_per_page)

    # Pegar o número da página atual da URL (GET request)
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    return render(request, 'receipts/receipts.html', {
        'months': months,
        'page_obj': page_obj
        })




