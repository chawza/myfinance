from django.db import models
from django.utils import timezone

# Create your models here.

class BudgetItem(models.Model):
    name = models.CharField(max_length=256, help_text="Item name or title")
    description = models.TextField()
    amount = models.IntegerField() 
    target = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    class Status(models.Model):
        CREATED = 0, 'Created'
        ONGOING = 1, 'On Going' 
        CANCELED = 2, 'Canceled'
        FINISH = 3, 'Finish'
        REALOCATED = 4, 'Realocated'
    status = models.PositiveSmallIntegerField(default=Status.CREATED)

    class Currency(models.IntegerChoices):
        IDR = 0, "IDR"
    currency = models.PositiveSmallIntegerField(Currency.choices, default=Currency.IDR)
    
    class Repetion(models.IntegerChoices):
        ONCE = 0, 'Once a day'
        DAILIY = 1, 'Daily'
        WEEKLY = 2, 'Weekly'
        MONTHLY = 3, 'Monthly'
        YEARLY = 4, "Yearly"
    repeat = models.PositiveSmallIntegerField(choices=Repetion.choices, default=Repetion.ONCE)
