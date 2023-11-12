from django.contrib import admin
from wallet.models import Transaction, Account, Label
from wallet.dashboards.models import AccountAdmin, TransactionAdmin, LabelAdmin

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Label, LabelAdmin)
