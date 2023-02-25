from django.db import models
from django.contrib.auth.models import User
from enum import Enum 
from datetime import datetime

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
    category = models.CharField(max_length=256)
    amount = models.FloatField()
    type = models.CharField(max_length=256, choices=Type.choices)
    note = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f'[{self.account.name}]:{self.date.isoformat()}\tAmount: {self.account.currency}{self.amount}'

class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_from')
    target_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_target')
    amount = models.FloatField()
