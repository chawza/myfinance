from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django import http
from wallet.models import Transaction, Transfer
from wallet.forms import GetTransactionForm
from datetime import datetime, timedelta
from operator import itemgetter
import json

def _parse_date(str_date: str | None, default: datetime) -> datetime:
    if str_date is None:
        return default
    else:
        return datetime.strptime(str_date, '%Y-%m-%d')
    
def _create_start_date(day_from_now = 3*30):
        return datetime.today() - timedelta(days=day_from_now)

def get_transaction_history(req: HttpRequest):
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
    else:
        return http.HttpResponseBadRequest(f'Inavalid [{req.method}] method')