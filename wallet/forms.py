from django import forms
from wallet.models import Transaction, User, Account
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from typing import List

class GetTransactionForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

class CreateNewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'note', 'date']

class UpdateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'note', 'date']


