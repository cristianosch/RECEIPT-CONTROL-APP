from django.urls import path
from .views import FormAddReceiptView 
from . import views


urlpatterns = [
    path('add_manual_receipt/', FormAddReceiptView.as_view(), name='add_manual_receipt'),
    #path('add_manual_receipt/', views.form_add_receipt, name='add_manual_receipt'),
    
]