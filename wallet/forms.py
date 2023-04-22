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


class CreateNewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'note', 'date']

class UpdateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'note', 'date']


