from django.contrib import admin
from budget.models import BudgetItem

# Register your models here.

class BudgetItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(BudgetItem, BudgetItemAdmin)