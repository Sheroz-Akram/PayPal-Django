# Generated by Django 4.1.7 on 2023-03-19 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0007_usertransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertransaction',
            name='transaction_type',
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
