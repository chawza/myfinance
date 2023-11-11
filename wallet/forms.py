from typing import Any, Dict
from django import forms
from wallet.models import Transaction, Label, Account, Transfer
from wallet.widgets import ColorPickerWidget
from django.utils import timezone 


class AddTransactionForm(forms.Form):
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
        labels = self.cleaned_data['labels']
        new_transaction = Transaction.objects.create(
            amount=self.cleaned_data['amount'],
            type=self.cleaned_data['type'],
            note=self.cleaned_data['note'],
            date=self.cleaned_data['date'],
            account=self.cleaned_data['account'],
        )
        if labels:
            new_transaction.labels.add(*labels)
    
class EditTransactionForm(AddTransactionForm):
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

class AbstractTransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Transfer.objects.all())
    target_account = forms.ModelChoiceField(queryset=Transfer.objects.all())
    amount = forms.IntegerField(initial=0)
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    note = forms.CharField(widget=forms.widgets.Textarea)

    def clean(self):
        if self.cleaned_data['from_account'] == self.cleaned_data['target_account']:
            raise forms.ValidationError('Target and Source Account cannot be the same!', code='same_src_target_account')


class AddTransferForm(AbstractTransferForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        users_account = Account.objects.filter(user=user)
        self.fields['from_account'].queryset = users_account
        self.fields['target_account'].queryset = users_account

    def save(self) -> Transfer:
        return Transfer.objects.create(
            user=self.user,
            from_account=self.cleaned_data['from_account'],
            target_account=self.cleaned_data['target_account'],
            amount=self.cleaned_data['amount'],
            date=self.cleaned_data['date'],
            note=self.cleaned_data['note'],
        )


class EditTransferForm(AbstractTransferForm):
    def __init__(self, transfer: Transfer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transfer = transfer

        self.fields['target_account'].initial = self.transfer.target_account
        self.fields['from_account'].initial = self.transfer.from_account
        self.fields['amount'].initial = self.transfer.amount
        self.fields['date'].initial = self.transfer.date
        self.fields['note'].initial = self.transfer.note
    
    def save(self) -> Transfer:
        self.transfer.target_account = self.cleaned_data['target_account']
        self.transfer.from_account = self.cleaned_data['from_account']
        self.transfer.amount = self.cleaned_data['amount']
        self.transfer.note = self.cleaned_data['note']
        self.transfer.date = self.cleaned_data['date']
        self.transfer.save()
        return self.transfer


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
    