from django import forms
from wallet.models import Transaction, Label
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
    labels= forms.ModelChoiceField(queryset=Label.objects.filter(), required=False) 
    amount = forms.IntegerField(min_value=0)
    type = forms.ChoiceField(choices=Transaction.Type.choices, initial=Transaction.Type.EXPENSES)
    note = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.labels.queryset = Label.objects.filter(owner=user)

    def save(self):
        return Transaction.objects.create(
            category=self.cleaned_data['labels'],
            amount=self.cleaned_data['amount'],
            type=self.cleaned_data['type'],
            note=self.cleaned_data['note'],
            date=self.cleaned_data['date'],
        )

class UpdateTransactionForm(CreateNewTransactionForm):
    def __init__(self, record: Transaction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.record = record
        self.fields['labels'].initial = record.labels
        self.fields['amount'].initial = record.amount
        self.fields['type'].initial = record.type
        self.fields['note'].initial = record.note
        self.fields['date'].initial = record.date

    def save(self):
        self.record.update(**self.cleaned_data)
