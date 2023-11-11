from django.contrib import admin
from wallet.models import Transaction, Account, Label


class TransactionAdmin(admin.ModelAdmin):
    ordering = ['-date',]
    list_display = ["note", "account", "amount", "date"]
    list_filter = ["account", "is_transfer"]

class AccountAdmin(admin.ModelAdmin):
    pass

class TransferAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Label)
