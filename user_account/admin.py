from django.contrib import admin

# Register your models here.
from user_account.models import UserProfile, UserPoint


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'work_type', 'service_city')
    search_fields = ('user', 'email', 'work_type', 'service_city')
    list_per_page = 300


class UserPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'created_at','updated_at')
    search_fields = ('user',)
    list_per_page = 300



admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(UserPoint, UserPointAdmin)
