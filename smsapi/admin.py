from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, PhoneNumber

# Register your models here.
admin.site.register(Account, UserAdmin)
admin.site.register(PhoneNumber)
