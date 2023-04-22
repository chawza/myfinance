from django.contrib.auth.models import User
from typing import List, Tuple

from wallet.models import Transaction, Account, Transfer
from wallet.scripts.reader import TransactionReader, TransactionRow

def populate_accounts(user: User, reader: TransactionReader):
    account_names = reader.get_all_acount_names()
    counter = 0
    for account_name in account_names:
        Account(user=user, name=account_name, currency=Account.CURRENCY_CHOICE[0][1]).save()
        print('Account: ', account_name)
        counter += 1
    
    print(f'Account Added: {counter}/{len(account_names)}')

def populate_transactions(user: User, reader: TransactionReader):
    transaction_read = 0
    transaction_added = 0

    for transaction in reader.read_transactions():
        transaction_read += 1

        account = Account.objects.get(user=user, name=transaction.account)
        transaction_type = transaction.type.upper()
        new_account = Transaction(
            account=account,
            category=transaction.category,
            amount=transaction.amount,
            note=transaction.note,
            date=transaction.date,
            type=transaction_type,
        )
        new_account.save()

        transaction_added += 1

    print(f'Transaction Added: {transaction_added}/{transaction_read}')

def _find_pair(element: TransactionRow, array: List[TransactionRow]):
    for el in array:
        if element.date == el.date and abs(element.amount) == abs(el.amount):
            return el
    return None 

def populate_transfers(user: User, reader: TransactionReader):
    read_count = 0
    transfer_added = 0

    transactions = [a for a in reader.read_transfers()]
    trans_temp: List[TransactionRow] = []

    transfer_pair: List[Tuple[TransactionRow, TransactionRow]] = []

    for trans in transactions:
        read_count += 1
        res = _find_pair(trans, trans_temp)
        if res:
            transfer_pair.append((trans, res))
            trans_temp.remove(res)
        else:
            trans_temp.append(trans)

    for src, trgt in transfer_pair:
        if trgt.amount < src.amount:
            src, trgt = trgt, src
        
        src_account = Account.objects.get(name=src.account)
        trgt_account = Account.objects.get(name=trgt.account)
        
        Transfer(user=user, amount=abs(src.amount), from_account=src_account, target_account=trgt_account).save()
        transfer_added += 1

    print(f'Transfer Added: {transfer_added}({transfer_added*2}/{read_count})')
    print(f'trans_temp remains: {len(trans_temp)}')
