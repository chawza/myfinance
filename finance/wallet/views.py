from django.shortcuts import render
from django.http import HttpRequest
from wallet.models import Transaction, Transfer
# Create your views here.

def get_transaction_history(req: HttpRequest):
    pass