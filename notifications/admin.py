from django.contrib import admin
from .models import Notification
# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient_user', 'sender_user', 'created_at', 'about_notifications','is_seen')
    search_fields = ('user','is_seen')
    list_per_page = 300


admin.site.register(Notification, NotificationAdmin)