import json

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.views import View

from finance.api import status
from django.contrib import messages

from wallet.models import Transaction, Transfer, User, Account
from wallet.forms import GetTransactionsForm, CreateNewTransactionForm, UpdateTransactionForm
    
def index(req: HttpRequest):
    context = {
        "records": Transaction.objects.all() or []
    }
    return render(req, 'wallet/index.html', context)

def add_record(req: HttpRequest):
    form = CreateNewTransactionForm(data=req.POST) 

    if req.POST:
        if form.is_valid():
            form.save()
            return redirect(reversed('wallet:home'))
        else:
            messages.error(req, message=form.errors.as_text()) 

    context = {
        "form": form 
    }
    return render(req, 'wallet/edit_record.html', context)

def update_record(req: HttpRequest, id):
    try:
        record = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        return HttpResponseBadRequest({"message": f"Pk not found {id}"})

    form = UpdateTransactionForm(record=record, data=req.POST) 

    if req.POST:
        if form.is_valid():
            form.save()
            return redirect(reversed('wallet:home'))
        else:
            messages.error(req, message=form.errors.as_text()) 

    context = {
        "form": form,
        "mode": "update"
    }
    return render(req, 'wallet/edit_record.html', context)
