from django.contrib import admin
from wallet.models import Transaction, Account, Transfer, Label


class TransactionAdmin(admin.ModelAdmin):
    ordering = ['-date',]

class AccountAdmin(admin.ModelAdmin):
    pass

class TransferAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Transfer, TransactionAdmin)
admin.site.register(Label)
