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

class TransactionReader:
    def __init__(self, filepath: str):
        extenstion = filepath.split('.')[-1]
        if extenstion == 'csv':
            self.df = pd.read_csv(filepath, delimiter=';')
        else:
            self.df = pd.read_excel(filepath)

    def _parse_date(self, value) -> datetime:
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif type(value) is float:
            return datetime.fromtimestamp(value)
        elif type(value) is int:
            return datetime.fromordinal(value)
        elif type(value) is datetime:
            return value
        else:
            raise Exception(f"Cannot parse :{type(value)}")
    
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
                date=self._parse_date(row['date']),
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
                date=self._parse_date(row['date']),
                type=row['type']
            )

    def get_all_acount_names(self):
        return self.df['account'].unique()