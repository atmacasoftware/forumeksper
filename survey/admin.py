from django.contrib import admin

from survey.models import Survey, Options, Vote

# Register your models here.

class OptionInline(admin.TabularInline):
    model = Options
    readonly_fields = ('options',)
    extra = 1
    show_change_link = True


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'created_user', 'created_at')
    search_fields = ('room','title','created_user')
    list_per_page = 300
    inlines = [OptionInline]

class OptionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'options', 'options_user', 'created_at')
    search_fields = ('survey','options','options_user')
    list_per_page = 300


class VoteAdmin(admin.ModelAdmin):
    list_display = ('survey', 'options', 'answered_user', 'is_answered')
    search_fields = ('survey','options','answered_user')
    list_per_page = 300

admin.site.register(Survey,SurveyAdmin)
admin.site.register(Options,OptionAdmin)
admin.site.register(Vote,VoteAdmin)