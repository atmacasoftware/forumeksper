from django.contrib import admin
from server.models import *
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'created_at','modified_at','is_private')
    search_fields = ('name','user')
    list_per_page = 300

class MemberAdmin(admin.ModelAdmin):
    list_display = ('group_user', 'room')
    search_fields = ('group_user','room')
    list_per_page = 300


class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date_added')
    search_fields = ('room','user')
    list_per_page = 300

admin.site.register(Room,RoomAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(MemberShip,MemberAdmin)
admin.site.register(RoomCategory)
