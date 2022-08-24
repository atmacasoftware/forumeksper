from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from mainpage.models import Citys, WorkType
from mainpage.resources import CityResource


# Register your models here.

class CityAdmin(ImportExportModelAdmin):
    list_display = ('id','name')
    resource_class = CityResource
    search_fields = ('name',)

admin.site.register(Citys, CityAdmin)
admin.site.register(WorkType)