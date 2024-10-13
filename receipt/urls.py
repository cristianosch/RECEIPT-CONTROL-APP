from django.urls import path
from . import views
#from .views import ChartDataView
from .views import DashboardView, CategoryTable

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    #path('', ChartDataView.as_view(), name='dashboard'),
    path('add-receipt', views.add_receipt, name='add-receipt'),
    path('receipts/', views.receipts, name='receipts'),
    path('receipts/edit/<int:pk>/', views.edit_receipt, name='edit_receipt'),
    path('receipts/<int:year>/<int:month>/', views.receipts_by_month, name='receipts_by_month'),
    path('category_information', CategoryTable.as_view(), name='category_information'),    
    #path('confirm-receipt-data/<int:receipt_id>/', views.confirm_receipt_data, name='confirm_receipt_data'),      
]