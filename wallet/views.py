from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http.request import HttpRequest
from django.contrib import messages
from django.forms import model_to_dict
from django.urls import reverse
from django.core.paginator import Paginator

from itertools import chain

from wallet.models import Transaction, Account, Transfer
from wallet import forms

    
def index(req: HttpRequest):
    accounts = req.user.accounts.all()
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
    transfers = Transfer.objects.filter(user=req.user).order_by('-date')

    records = chain(transactions, transfers)
    records = sorted(records, key=lambda x: x.date, reverse=True)

    records = Paginator(records, 20)
    current_page = int(req.GET.get('page', 1))
    current_page = current_page if current_page <= records.num_pages else 1
    page = records.page(current_page)

    context = {
        "records": page
    }
    return render(req, 'wallet/index.html', context)

def add_record(req: HttpRequest):
    transaction_form = forms.AddTransactionForm(user=req.user, data=req.POST) 
    transfer_form = forms.AddTransferForm(user=req.user, data=req.POST)

    if req.POST:
        form_type = req.POST.get('form', None)
        if form_type in ['transaction', 'transfer']:
            if form_type == 'transaction':
                if transaction_form.is_valid():
                    transaction_form.save()
                    messages.info(req, 'New Transaction has been added!')
            else:
                if transfer_form.is_valid():
                    transfer_form.save()
                    messages.info(req, 'New Transfer has been added!')
        else:
            messages.error(req, message="Unrecognized Form Type")

    context = {
        "transaction_form": transaction_form,
        "transfer_form": transfer_form, 
    }
    return render(req, 'wallet/edit_record.html', context)

def update_record(req: HttpRequest, id):
    try:
        record = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        messages.error(req, message=f"record with id {id} is not found")
        return redirect(reverse('wallet:home'))
    
    if req.POST:
        extra_data = {'data': req.POST}
    else:
        extra_data = {'initial': model_to_dict(record, exclude=['id'])}
    
    form = forms.EditTransactionForm(
        user=req.user,
        record=record,
        **extra_data
    )

    if req.POST:
        if form.is_valid():
            form.save()
            return redirect(reverse('wallet:home'))
        else:
            messages.error(req, message=form.errors.as_text()) 

    context = {
        "form": form,
        "mode": "update"
    }
    return render(req, 'wallet/edit_record.html', context)

def accounts(req: HttpRequest):
    context = {
        'accounts': Account.get_account_list_from(req.user) 
    }
    return render(req, 'wallet/accounts.html', context)

def add_account(req: HttpRequest):
    form = forms.CreateAccount(user=req.user, data=req.POST)

    if req.POST:
        if form.is_valid():
            new_account = form.save()
            messages.info(req, f'Account "{new_account.name}" has been CREATED!')
            return redirect(reverse('wallet:accounts'))
        else:
            messages.error(req, form.errors.as_text())

    return render(req, 'wallet/edit_account.html', context={'form': form}) 


def update_account(req: HttpRequest, id: int):
    try:
        account = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        messages.error(f'Account does not exist!')
        return redirect(reverse('accounts'))

    if req.POST:
        extra_data = {'data': req.POST}
    else:
        extra_data = {'initial': model_to_dict(account, exclude=['id'])}

    form = forms.UpdateAccount(account=account, data=req.POST, **extra_data)

    if req.POST:
        if form.is_valid():
            form.save()
            messages.info(req, f'Account "{account.name}" has been UPDATED!')
            return redirect(reverse('wallet:accounts'))
        else:
            messages.error(req, form.errors.as_text())
    
    context = {
        'form': form,
        'mode': 'update'
    }

    return render(req, 'wallet/edit_account.html', context=context)
