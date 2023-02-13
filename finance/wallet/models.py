from django.db import models
from django.contrib.auth.models import User
from enum import Enum 
from datetime import datetime

class Account(models.Model):
    CURRENCY_CHOICE = (
        ('IDR', 'Indonesia Rupiah'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    currency = models.CharField(max_length=256, choices=CURRENCY_CHOICE, default=CURRENCY_CHOICE[0][1])

class Transaction(models.Model):
    class Type(models.TextChoices):
        EXPENSES = 'Expenses'
        INCOME = 'Income'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE) 
    category = models.CharField(max_length=256)
    amount = models.FloatField()
    type = models.CharField(max_length=256, choices=Type.choices)
    note = models.TextField()
    date = models.DateTimeField()

    def serialize(self):
        return {
            'user_id': self.user.id,
            'account': self.account.name,
            'category': self.category,
            'amount':self.category,
            'type': self.type,
            'note': self.note,
            'date': datetime.strftime(self.date, '%Y-%m-%d %H:%M:%S')
        }

class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='source_account')
    target_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='target_account')
    amount = models.FloatField()

