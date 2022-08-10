from django.contrib import admin
from server.models import *
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'user','created_at','modified_at','is_private')
    search_fields = ('name','user')
    list_per_page = 300

class MemberAdmin(admin.ModelAdmin):
    list_display = ('group_user', 'room')
    search_fields = ('group_user','room')
    list_per_page = 300

admin.site.register(Room,RoomAdmin)
admin.site.register(Message)
admin.site.register(MemberShip,MemberAdmin)
