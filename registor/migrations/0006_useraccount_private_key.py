# Generated by Django 4.1.7 on 2023-03-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0005_alter_useraccount_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='private_key',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
