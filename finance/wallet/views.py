from operator import itemgetter
from datetime import datetime, timedelta
import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django import http
from django.views.decorators.csrf import ensure_csrf_cookie 

from wallet.models import Transaction, Transfer, User, Account
from wallet.forms import GetTransactionForm, CreateNewTransactionForm, UpdateTransactionForm

def _parse_date(str_date: str | None, default: datetime) -> datetime:
    if str_date is None:
        return default
    else:
        return datetime.strptime(str_date, '%Y-%m-%d')
    
def _create_start_date(day_from_now = 3*30):
        return datetime.today() - timedelta(days=day_from_now)

def handle_transactions(req: HttpRequest):
    if req.method == 'GET':
        queries = {
            'start_date': req.GET.get('start_date', _create_start_date(30)),
            'end_date': req.GET.get('end_date', datetime.today())
        }

        form = GetTransactionForm(queries)

        if not form.is_valid():
            response_payload = form.errors.as_json()
            return HttpResponseBadRequest(content=response_payload)
        
        start_date, end_date = itemgetter('start_date','end_date')(form.cleaned_data)

        transactions = Transaction.objects\
            .filter(date__gte=start_date)\
            .filter(date__lte=end_date)\
            .order_by('-date', )

        payload = {
            'user_id': transactions[0].user.id,
            'count': transactions.count(),
            'transactions': [{
                'account_id': tran.account.id,
                'category': tran.category,
                'amount': tran.amount,
                'note': tran.note,
                'date': datetime.strftime(tran.date, '%Y-%m-%d %H:%M:%S')
            } for tran in transactions]
        } 
        return HttpResponse(content=json.dumps(payload))

    if req.method == 'POST':
        body = json.loads(req.body.decode())
        form = CreateNewTransactionForm(body)

        if not form.is_valid():
            response_payload = form.errors.as_json()
            return HttpResponseBadRequest(content=response_payload)

        new_transaction = Transaction(
            user=User.objects.get(id=body['user_id']),
            account=Account.objects.get(id=body['account_id']),
            **form.cleaned_data
        )
        new_transaction.save()
        
        return HttpResponse('transaction created')

    else:
        return http.HttpResponseBadRequest(f'Inavalid [{req.method}] method')

def handle_transaction_model(req: HttpRequest, id: int):
    body = json.loads(req.body.decode())

    transaction_id = body['id']
    try:
        user_has_transaction(req.user, transaction_id)
    except Transaction.DoesNotExist:
        return http.HttpResponseBadRequest(f'User does not have transaction with id {transaction_id}')

    if req.method == 'UPDATE':
        form = UpdateTransactionForm(**body)
        
        if not form.is_valid():
            response_payload = form.errors.as_json()
            return HttpResponseBadRequest(content=response_payload)

        form.save()

        return HttpResponse('transaction saved!')

    elif req.method == 'DELETE':
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.delete()
    else:
        return http.HttpResponseBadRequest(f'Inavalid [{req.method}] method')
    

def user_has_transaction(user: User, transaction_id):
    for account in user.accounts:
        transaction = account.transactions.filter(id=transaction_id).first()
        if transaction is not None:
            return True
    return False
