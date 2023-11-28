from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.monthly_summary, name='home'),

    # Records
    path('add', views.add_record, name='add_record'),
    path('update/<int:id>', views.update_record, name='update_record'),

    # Accounts
    path('accounts', views.accounts, name='accounts'),
    path('add-account', views.add_account, name='add_account'),
    path('update-account/<int:id>', views.update_account, name='update_account'),
]
