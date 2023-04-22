from operator import itemgetter
from datetime import datetime, timedelta
import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie 
from django.views import View

from finance.api import status

from wallet.models import Transaction, Transfer, User, Account
from wallet.forms import GetTransactionsForm

class TransactionAPIView(View):
    def get(self, req: HttpRequest, id: int):
        transaction = Transaction.objects.get(id=id)
        if not transaction:
            return HttpResponseBadRequest(status=status.HTTP_ERROR_NOT_FOUND)
        return JsonResponse(data=transaction.serialize()) 

class TransactionsAPIView(View):

    def get(self, req: HttpRequest):
        form = GetTransactionsForm(data=req.GET)

        if form.is_valid():
            page, paginate = form.page, form.paginate
            transactions = (
                Transaction.objects
                .filter(date__gte=form.start_date, date__lete=form.end_date)
                .order_by(form.order)
            )
            # Paginate
            # TODO: serilize data better
            data = {
                "data": [tran.serialize() for tran in transactions] if transactions else [],
                "count": transactions.count(),
                "page": page,
                "paginate": paginate
            }

            return HttpResponse(content=json.dumps(data))
        
        return HttpResponseNotAllowed("invalid parameter")
