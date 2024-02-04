from django.contrib import admin
from registor.models import UserAccount
from registor.models import UserTransaction
from registor.models import UserNotification

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserTransaction)
admin.site.register(UserNotification)