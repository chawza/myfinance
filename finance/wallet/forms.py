from django import forms
from wallet.models import Transaction

class GetTransactionForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

class CreateNewTransaction(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'note', 'date']
