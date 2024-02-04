from django.db import models

# Create your models here.


# This Model Store User Data
class UserAccount(models.Model):
    notification_count = models.DecimalField(max_digits=10, decimal_places=0 , default=0)
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    currency_type = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    private_key = models.CharField(max_length=64, blank=True)

class UserTransaction(models.Model):
    transaction_date = models.DateField()
    sender_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    receiver_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    to_person = models.CharField(max_length=100)
    from_person = models.CharField(max_length=100)
    sender_balance = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_balance = models.DecimalField(max_digits=10, decimal_places=2)

class UserNotification(models.Model):
    notification_receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    notification_date = models.DateField()
    notification_msg = models.TextField()
    notificatoin_type = models.CharField(max_length=100)
    other_person = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)