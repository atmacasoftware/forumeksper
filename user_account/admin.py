from django.contrib import admin

# Register your models here.
from user_account.models import UserProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email','work_type','service_city')
    search_fields = ('user','email','work_type','service_city')
    list_per_page = 300

admin.site.register(UserProfile, ProfileAdmin)