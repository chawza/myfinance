from django.contrib import admin
from django.utils.html import format_html
from wallet.models import Transaction, Account, Label


class TransactionAdmin(admin.ModelAdmin):
    ordering = ['-date',]
    list_display = ["note", "account", "amount_decimal", "date"]
    list_filter = ["account", "is_transfer"]

    @admin.display(description="amount")
    def amount_decimal(self, obj: Transaction):
        style = ""

        if obj.is_transfer:
            style = ' style="color: #888888";'

        return format_html(f'<div{style}>{obj.amount:,.0f}</div>')

class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "balance_decimal"]

    @admin.display(description="balance")
    def balance_decimal(self, obj: Account):
        return f'{obj.balance():,.0f}'

class TransferAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Label)
