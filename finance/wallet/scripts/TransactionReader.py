import pandas as pd
from datetime import datetime
from dataclasses import dataclass

@dataclass
class TransactionRow:
    account: str
    category: str
    amount: float
    is_transfer: str
    note: str
    date: datetime
    type: str

class TransactionReader():
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath, delimiter=';')
    
    def read_transactions(self):
        for idx, row in self.df.iterrows():
            if bool(row['transfer']) == True:
                continue
            yield TransactionRow(
                account=row['account'],
                category=row['category'],
                amount=float(row['amount']),
                is_transfer=bool(row['transfer']),
                note=row['note'],
                date=datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'),
                type=row['type']
            )

    def read_transfers(self):
        for idx, row in self.df.iterrows():
            if bool(row['transfer']) == False:
                continue
            yield TransactionRow(
                account=row['account'],
                category=row['category'],
                amount=float(row['amount']),
                is_transfer=bool(row['transfer']),
                note=row['note'],
                date=datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'),
                type=row['type']
            )

    def get_all_acount_names(self):
        return self.df['account'].unique()