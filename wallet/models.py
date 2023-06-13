from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    CURRENCY_CHOICE = (
        ('IDR', 'Indonesia Rupiah'),
    )
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=256)
    currency = models.CharField(max_length=256, choices=CURRENCY_CHOICE, default=CURRENCY_CHOICE[0][1])
        
class Transaction(models.Model):
    class Type(models.TextChoices):
        EXPENSES = 'Expenses'
        INCOME = 'Income'
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions') 
    # category = models.ForeignKey('wallet.Label', on_delete=models.CASCADE, related_name='categories')
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

class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_from')
    target_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_target')
    amount = models.FloatField()

class Label(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='labels', on_delete=models.CASCADE)
