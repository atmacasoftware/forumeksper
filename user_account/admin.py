from django.contrib import admin

# Register your models here.
from user_account.models import UserProfile

admin.site.register(UserProfile)