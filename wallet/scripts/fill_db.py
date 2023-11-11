from django.contrib.auth.models import User
from typing import List, Tuple

from wallet.models import Transaction, Account, Label
from wallet.scripts.reader import TransactionReader, TransactionRow

def populate_accounts(user: User, reader: TransactionReader):
    account_names = reader.get_all_acount_names()
    counter = 0
    for account_name in account_names:
        Account(user=user, name=account_name, currency=Account.CURRENCY_CHOICE[0][1]).save()
        print('Account: ', account_name)
        counter += 1
    
    print(f'Account Added: {counter}/{len(account_names)}')

def pouplate_category(user: User, reader: TransactionReader):
    categories = reader.get_categories()
    for category in categories:
        Label.objects.create(name=category, owner=user)
    print('Categories : ', len(categories))
    

def populate_transactions(user: User, reader: TransactionReader):
    transaction_read = 0
    transaction_added = 0

    for transaction in reader.read_transactions():
        transaction_read += 1

        account = Account.objects.get(user=user, name=transaction.account)
        tran_type = Transaction.Type.EXPENSES if transaction.type.lower() == 'expenses' else Transaction.Type.INCOME
        label = Label.objects.get(name=transaction.category)
        new_account = Transaction(
            account=account,
            amount=transaction.amount,
            note=transaction.note,
            date=transaction.date,
            type=tran_type,
            is_transfer=transaction.is_transfer
        )
        new_account.save()
        new_account.labels.add(label)

        transaction_added += 1

    print(f'Transaction Added: {transaction_added}/{transaction_read}')

def delete_user_data(user: User):
    _, count = Label.objects.filter(owner=user).delete()
    print('labels deleted ', count)
    _, count = user.accounts.all().delete()
    print('accounts deleted ', count)
