# Generated by Django 4.1.7 on 2023-03-21 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0013_usernotification_notification_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotification',
            name='notification_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registor.useraccount'),
        ),
    ]