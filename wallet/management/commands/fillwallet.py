from io import StringIO
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser
from django.db.transaction import atomic
from wallet.models import User

from wallet.scripts import fill_db, reader

class Command(BaseCommand):
    help = "Fill database with /wallet related models"
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'username',
            type=str,
            help='username for target filling'
        )

        parser.add_argument(
            'filepath',
            type=str,
            help='Source filepath'
        )
        
        parser.add_argument(
            "--transactions",
            action='store_true',
            help="Transactions data filepath",
        )

        parser.add_argument(
            "--accounts",
            action='store_true',
            help="Accounts data filepath",
        )

        parser.add_argument(
            "--transfers",
            action='store_true',
            help="Transfers data filepath",
        )

        parser.add_argument(
            '--all',
            action='store_true',
            help="fille all",
        )

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        username = options.get('username', None)
        filepath = options.get('filepath', None)
        all_models = options.get('all', None)

        if not username:
            raise Exception("Pleaser specify `username`!")
        
        if not filepath:
            raise Exception('Please specify `filepath`!')

        user: User = User.objects.get(username=username)
        if not user:
            raise Exception(f"User with username: {username} is not found!") 

        transaction_reader = reader.TransactionReader(filepath=filepath)
        if options.get('accounts', None) or all_models:
            fill_db.populate_accounts(user, transaction_reader)

        if options.get('transactions', None) or all_models:
            fill_db.populate_transactions(user, transaction_reader)

        if options.get('transfers', None) or all_models:
            fill_db.populate_transfers(user, transaction_reader)
