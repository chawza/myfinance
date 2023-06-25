from typing import Any, Dict
from django import forms
from wallet.models import Transaction, Label, Account
from wallet.widgets import ColorPickerWidget


class CreateNewTransactionForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.filter())
    labels = forms.ModelMultipleChoiceField(queryset=Transaction.objects.filter(), widget=forms.SelectMultiple)
    amount = forms.IntegerField(min_value=0)
    type = forms.ChoiceField(choices=Transaction.Type.choices, initial=Transaction.Type.EXPENSES)
    note = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        self.fields['labels'].queryset = Label.objects.filter(owner=user)

    def save(self):
        return Transaction.objects.create(
            labels=self.cleaned_data['labels'],
            amount=self.cleaned_data['amount'],
            type=self.cleaned_data['type'],
            note=self.cleaned_data['note'],
            date=self.cleaned_data['date'],
            account=self.cleaned_data['account'],
        )

class UpdateTransactionForm(CreateNewTransactionForm):
    def __init__(self, user, record: Transaction, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.record = record

    def save(self):
        self.record.account = self.cleaned_data['account']
        self.record.labels = self.cleaned_data['labels']
        self.record.amount = self.cleaned_data['amount']
        self.record.type = self.cleaned_data['type']
        self.record.note = self.cleaned_data['note']
        self.record.date = self.cleaned_data['date']
        self.record.save()

class AccountForm(forms.Form):
    name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Account Name'}))
    color = forms.CharField(widget=ColorPickerWidget, initial='#808080')


class CreateAccount(AccountForm):
    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self) -> Account:
        return Account.objects.create(user=self.user, name=self.cleaned_data['name'])
    
class UpdateAccount(AccountForm):
    name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Account Name'}))
    color = forms.CharField(widget=ColorPickerWidget, initial='#808080')

    def __init__(self, account: Account, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.account = account

    def save(self) -> None:
        self.account.name = self.cleaned_data['name']
        self.account.save(update_fields=['name'])
    