from django.urls import path
from . import views

urlpatterns = [
    path('transactions', views.get_transaction_history, name='Get Transactions')
]