# Generated by Django 4.1.7 on 2023-03-21 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0015_usernotification_notificatoin_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
