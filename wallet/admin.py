from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.forms import ModelForm
from django.forms.widgets import TextInput
from wallet.models import Transaction, Account, Label
from rangefilter.filters import DateRangeFilterBuilder


class AccountAdminForm(ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        widgets = {"color": TextInput(attrs={"type": "color"})}


class LabelAdminForm(ModelForm):
    class Meta:
        model = Label
        fields = "__all__"
        widgets = {"color": TextInput(attrs={"type": "color"})}

class TransactionAccountFilter(admin.SimpleListFilter):
    title = "Account"
    parameter_name = "account"

    def lookups(self, request: HttpRequest, model_admin: Any) -> list[tuple[Any, str]]:
        accounts = Account.objects.all()

        if not request.user.is_superuser:
            accounts = accounts.filter(user=request.user)

        if request.user.is_superuser:
            return

        for account in accounts:
            yield (account.id, account.name)

    def queryset(self, request: HttpRequest, queryset: QuerySet[Transaction]) -> QuerySet[Any] | None:
        if not request.user.is_superuser:
            queryset = queryset.filter(account__user=request.user)

        if not self.value():
            return queryset

        return queryset.filter(account=self.value())

class TransactionAdmin(admin.ModelAdmin):
    start_date_range = DateRangeFilterBuilder('Date Range')

    ordering = ['-date',]
    list_display = ["note", "custom_account", "amount_decimal", "date"]
    list_filter = [TransactionAccountFilter, "is_transfer", ("date", start_date_range)]
    list_select_related = ["account"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Transaction]:
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(account__in=request.user.accounts.all())
        return qs

    @admin.display(description="amount")
    def amount_decimal(self, obj: Transaction):
        style = ""

        if obj.is_transfer:
            style = ' style="color: #888888";'

        return format_html(f'<div{style}>{obj.amount:,.0f}</div>')
    
    @admin.display(description="account")
    def custom_account(self, obj: Transaction):
        style = ""

        if obj.account.color:
            style = f' style="color: {obj.account.color}";'

        return format_html(f'<div{style}>{obj.account.name}</div>')
        

class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "balance_decimal"]
    form = AccountAdminForm

    def get_queryset(self, request: HttpRequest) -> QuerySet[Transaction]:
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

    @admin.display(description="balance")
    def balance_decimal(self, obj: Account):
        return f'{obj.balance():,.0f}'
    
class LabelAdmin(admin.ModelAdmin):
    form = LabelAdminForm

    def get_queryset(self, request: HttpRequest) -> QuerySet[Label]:
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Label, LabelAdmin)
