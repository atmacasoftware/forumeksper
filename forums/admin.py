from django.contrib import admin
from .models import *
# Register your models here.

class ForumAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'created_at','status')
    search_fields = ('user','status','category')
    list_per_page = 300

class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'status')
    search_fields = ('name','status')
    list_per_page = 300

class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum','created_at','status')
    search_fields = ('user','forum','status')
    list_per_page = 300

class ForumViewAdmin(admin.ModelAdmin):
    list_display = ('forum', 'ip_address')
    search_fields = ('forum','ip_address')
    list_per_page = 300

class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'forums','created_at','status')
    search_fields = ('user','forums','status')
    list_per_page = 300

class LikeForumAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum','ip','is_liked','created_at')
    search_fields = ('user','forum','ip','is_liked')
    list_per_page = 300

class DisLikeForumAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum','ip','is_liked','created_at')
    search_fields = ('user','forum','ip','is_liked')
    list_per_page = 300

class LikeCommentAdmin(admin.ModelAdmin):
    list_display = ('user','ip','is_liked','created_at')
    search_fields = ('user','ip','is_liked')
    list_per_page = 300

class DisLikeCommentAdmin(admin.ModelAdmin):
    list_display = ('user','ip','is_liked','created_at')
    search_fields = ('user','ip','is_liked')
    list_per_page = 300

class EditorSelectAdmin(admin.ModelAdmin):
    list_display = ('forum', 'is_active', 'created_at')
    search_fields = ('forum','is_active')
    list_per_page = 300

admin.site.register(Forum,ForumAdmin)
admin.site.register(ForumCategory,ForumCategoryAdmin)
admin.site.register(ForumComment,ForumCommentAdmin)
admin.site.register(ForumView,ForumViewAdmin)
admin.site.register(ReplyComment,ReplyCommentAdmin)
admin.site.register(LikeForum,LikeForumAdmin)
admin.site.register(DisLikeForum,DisLikeForumAdmin)
admin.site.register(LikeComment,LikeCommentAdmin)
admin.site.register(DisLikeComment,DisLikeCommentAdmin)
admin.site.register(EditorSelectForum,EditorSelectAdmin)
admin.site.register(UserForumPoint)
