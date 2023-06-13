import json

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http.request import HttpRequest
from django.contrib import messages

from wallet.models import Transaction
from wallet.forms import CreateNewTransactionForm, UpdateTransactionForm
    
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
        messages.error(req, message=f"record with id {id} is not found")
        return redirect(reversed('wallet:home'))

    form = UpdateTransactionForm(record=record) 

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
