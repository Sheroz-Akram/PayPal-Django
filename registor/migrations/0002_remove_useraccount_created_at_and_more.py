# Generated by Django 4.1.7 on 2023-03-18 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='created_at',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='currency_type',
            field=models.CharField(max_length=50),
        ),
    ]
