from django import forms

class GetTransactionForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    