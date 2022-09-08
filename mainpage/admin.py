from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from mainpage.models import Citys, WorkType, BankList, LoanInterestRate, Weather, NewsCategory
from mainpage.resources import CityResource,WeatherResource


# Register your models here.

class CityAdmin(ImportExportModelAdmin):
    list_display = ('id','name')
    resource_class = CityResource
    search_fields = ('name',)

class WeatherAdmin(ImportExportModelAdmin):
    list_display = ('city','ip')
    resource_class = WeatherResource
    search_fields = ('city','ip')


admin.site.register(Citys, CityAdmin)
admin.site.register(WorkType)
admin.site.register(BankList)
admin.site.register(LoanInterestRate)
admin.site.register(Weather,WeatherAdmin)
admin.site.register(NewsCategory)