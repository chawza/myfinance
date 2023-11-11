from django.db import models
from django.db.models import Sum, QuerySet, Q, F
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import timezone


class Account(models.Model):
    CURRENCY_CHOICE = (
        ('IDR', 'Indonesia Rupiah'),
    )
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    initial = models.IntegerField(default=0)
    name = models.CharField(max_length=256)
    currency = models.CharField(max_length=256, choices=CURRENCY_CHOICE, default=CURRENCY_CHOICE[0][1])
    color = models.CharField(max_length=7, default='#808080')

    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def get_account_list_from(cls, user: User) -> QuerySet['Account']:
        return (
            Account.objects.filter(user=user)
            .annotate(
                expense=Sum('transactions__amount', filter=Q(transactions__type=Transaction.Type.EXPENSES), default=0),
                income=Sum('transactions__amount', filter=Q(transactions__type=Transaction.Type.INCOME), default=0),
            )
            .annotate(
                balance=F('initial') + F('income') - F('expense')
            )
        )
    
    def balance(self) -> int:
        transactions: QuerySet[Transaction] = self.transactions
        cumulative_balance = (
            transactions
            .filter(date__lte=timezone.now())
            .aggregate(balance=Sum("amount", default=0))["balance"]
        )
        return self.initial + cumulative_balance
        
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions') 
    labels = models.ManyToManyField('wallet.Label', related_name='transactions')
    amount = models.IntegerField()
    note = models.TextField()
    date = models.DateTimeField()
    is_transfer = models.BooleanField(default=False)

    class Type(models.IntegerChoices):
        EXPENSES = 1, "Expenses"
        INCOME = 2, "Income"
    type = models.SmallIntegerField(choices=Type.choices, default=Type.EXPENSES)

    def __str__(self):
        return self.note
    
    def serialize(self):
        return {
            "account": self.account.id,
            "label": self.labels,
            "amount": self.amount,
            "type": self.get_type_display(),
            "note": self.note,
            "date": self.date.timestamp()
        }
    
    def render_html(self) -> str:
        return render_to_string('wallet/components/transaction.html', {'record': self})

class Label(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='labels', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
