from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from wallet.models import Transaction, Transfer
import json

def get_transaction_history(req: HttpRequest):
    trans_query = Transaction.objects.all()
    transactions = [tran.serialize() for tran in trans_query]
    payload = json.dumps(transactions)
    return HttpResponse(content=payload) 