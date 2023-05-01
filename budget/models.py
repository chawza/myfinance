from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class BudgetItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, help_text="Item name or title")
    description = models.TextField()
    amount = models.IntegerField(default=0) 
    target = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    target_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Status(models.IntegerChoices):
        CREATED = 0, 'Created'
        ONGOING = 1, 'On Going' 
        CANCELED = 2, 'Canceled'
        FINISH = 3, 'Finish'
        REALOCATED = 4, 'Realocated'
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.CREATED)

    class Currency(models.IntegerChoices):
        IDR = 0, "IDR"
    currency = models.PositiveSmallIntegerField(choices=Currency.choices, default=Currency.IDR)
    
    class Repetion(models.IntegerChoices):
        ONCE = 0, 'Once'
        DAILIY = 1, 'Daily'
        WEEKLY = 2, 'Weekly'
        MONTHLY = 3, 'Monthly'
        YEARLY = 4, "Yearly"
    repeat = models.PositiveSmallIntegerField(choices=Repetion.choices, default=Repetion.ONCE)

    def __str__(self):
        return f"{self.user.username}:{self.name}"
