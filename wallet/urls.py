from django.urls import path
from . import views

urlpatterns = [
    path('transaction/<int:id>', views.handle_transaction_model, name='Transaction CRUD'),
    path('transactions', views.handle_transactions, name='handle transactions'),
]