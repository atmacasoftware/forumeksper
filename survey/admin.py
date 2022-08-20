from django.contrib import admin

from survey.models import Survey, Options, Vote

# Register your models here.

admin.site.register(Survey)
admin.site.register(Options)
admin.site.register(Vote)