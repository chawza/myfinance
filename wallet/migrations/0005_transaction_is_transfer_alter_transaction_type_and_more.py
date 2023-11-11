# Generated by Django 4.1.6 on 2023-11-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_transfer_date_alter_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_transfer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'Expenses'), (2, 'Income')], default=1),
        ),
        migrations.DeleteModel(
            name='Transfer',
        ),
    ]
