# Generated by Django 4.1.6 on 2023-11-12 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_transaction_is_transfer_alter_transaction_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
