from django.db import models
from django.db.models import Sum, QuerySet, Q, F
from django.contrib.auth.models import User
from datetime import datetime
from django.template.loader import render_to_string


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
                transfer_out=Sum('transfers_target__amount', default=0),
                transfer_in=Sum('transfers_from__amount', default=0),
            )
            .annotate(
                expense=Sum('transactions__amount', filter=Q(transactions__type=Transaction.Type.EXPENSES), default=0),
                income=Sum('transactions__amount', filter=Q(transactions__type=Transaction.Type.INCOME), default=0),
            )
            .annotate(
                balance=F('initial') + F('transfer_in') + F('income') - F('transfer_out') - F('expense')
            )
        )
        
class Transaction(models.Model):
    class Type(models.TextChoices):
        EXPENSES = 0 
        INCOME = 1 
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions') 
    labels = models.ManyToManyField('wallet.Label', related_name='transactions')
    amount = models.IntegerField()
    type = models.SmallIntegerField(choices=Type.choices, default=Type.EXPENSES)
    note = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f'[{self.account.name}]:{self.date.isoformat()}\tAmount: {self.account.currency}{self.amount}'
    
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

class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_from')
    target_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_target')
    amount = models.FloatField()
    date = models.DateTimeField(default=datetime.now)
    note = models.TextField(default='')

    def render_html(self) -> str:
        return render_to_string('wallet/components/transfer.html', {'record': self})

class Label(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='labels', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
