# Generated by Django 4.1.7 on 2023-03-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0009_rename_total_amount_usertransaction_receiver_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='user_name',
            field=models.CharField(default='user', max_length=100),
            preserve_default=False,
        ),
    ]
