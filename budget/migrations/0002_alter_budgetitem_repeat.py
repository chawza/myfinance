# Generated by Django 4.1.6 on 2023-11-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetitem',
            name='repeat',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Once'), (1, 'Daily'), (2, 'Weekly'), (3, 'Monthly'), (4, 'Yearly')], default=0),
        ),
    ]
