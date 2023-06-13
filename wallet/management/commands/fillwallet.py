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
            '--reset',
            action='store_true',
            help="burn allc"
        )

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        username = options.get('username', None)
        filepath = options.get('filepath', None)
        reset = options.get('reset', None)

        if not username:
            raise Exception("Pleaser specify `username`!")
        
        if not filepath:
            raise Exception('Please specify `filepath`!')

        user: User = User.objects.get(username=username)
        if not user:
            raise Exception(f"User with username: {username} is not found!")

        if reset: 
            fill_db.delete_user_data(user)
        
        transaction_reader = reader.TransactionReader(filepath=filepath)
        fill_db.populate_accounts(user, transaction_reader)
        fill_db.pouplate_category(user, transaction_reader)
        fill_db.populate_transactions(user, transaction_reader)
        fill_db.populate_transfers(user, transaction_reader)
