import json

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.forms import model_to_dict
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from wallet.models import Transaction, Account
from wallet import forms

    
def index(req: HttpRequest):
    accounts = req.user.accounts.all()
    records = Transaction.objects.filter(account__in=accounts).order_by('-date')

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


@login_required
def monthly_summary(req: HttpRequest) -> HttpResponse:
    accounts = Account.objects.all() if req.user.is_superuser else req.user.accounts.all()
    qs = Transaction.objects.filter(account__user=req.user)

    today = timezone.now().date()
    form = forms.MonthlySummary(
        accounts=accounts, data=req.GET or None,
        initial={
            "end_date": today,
            "start_date": today.replace(day=1),
            "accounts": [acc.id for acc in accounts]
        }
    )

    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        accounts = form.cleaned_data['accounts']
    else:
        start = form.initial['start_date']
        end = form.initial['end_date']
        accounts = form.initial['accounts']

    datas = form.get_chart_data(qs, start, end, accounts)

    context = {
        "form": form,
        "chart_data": json.dumps(datas)
    }

    return render(req, 'wallet/monthly_summary.html', context=context)