# Generated by Django 4.1.6 on 2023-04-20 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_transaction_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
    ]