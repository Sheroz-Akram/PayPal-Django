# Generated by Django 4.1.7 on 2023-03-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registor', '0014_alter_usernotification_notification_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='notificatoin_type',
            field=models.CharField(default='Send', max_length=100),
            preserve_default=False,
        ),
    ]