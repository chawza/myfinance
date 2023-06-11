from django import forms
from wallet.models import Transaction, User, Account
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from enum import Enum
from typing import Dict, Any
from django.utils import timezone

DEFAULT_NUMBER_PER_PAGE = 20

class GetTransactionsForm(forms.Form):
    page = forms.IntegerField(initial=1)
    paginate = forms.IntegerField(initial=DEFAULT_NUMBER_PER_PAGE)
    start_date = forms.DateField(initial=timezone.now)
    end_date = forms.DateField(initial=timezone.now)
    order = forms.CharField(max_length=30)

    ORDER_CHOICES = ['date', '-date']

    def clean_order(self, value: str):
        if value not in self.ORDER_CHOICES:
            return forms.ValidationError(
                code='invalid_order_parameter'
            )
        return value

class CreateNewTransactionForm(forms.Form):
    category = forms.CharField()
    amount = forms.IntegerField(min_value=0)
    type = forms.ChoiceField(choices=Transaction.Type.choices, initial=Transaction.Type.EXPENSES)
    note = forms.CharField(widget=forms.Textarea())
    date = forms.DateField()

    def save(self):
        pass

class UpdateTransactionForm(CreateNewTransactionForm):
    def __init__(self, record: Transaction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.record = record 

    def save(self):
        self.record.update(**self.cleaned_data)


