from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from mainpage.models import Citys, WorkType, BankList, LoanInterestRate, Weather, NewsCategory, Advertisement, Note, AdsCategory, AdvertisementType,CreateAds
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


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company','email','phone','type','ads','created_at')
    search_fields = ('email','phone')
    list_per_page = 300

class NoteAdmin(admin.ModelAdmin):
    list_display = ('pages', 'created_at')
    search_fields = ('pages','created_at')
    list_per_page = 300

class AdsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','slug', 'created_at', 'update_at')
    search_fields = ('name','price')
    list_per_page = 50

class AdvertisementTypeAdmin(admin.ModelAdmin):
    list_display = ('name','slug', 'created_at', 'update_at')
    search_fields = ('name','created_at')
    list_per_page = 50

class CreateAdsAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'phone', 'price','category','is_time','created_at')
    search_fields = ('name','email','created_at','is_time')
    list_per_page = 300

admin.site.register(Citys, CityAdmin)
admin.site.register(WorkType)
admin.site.register(BankList)
admin.site.register(LoanInterestRate)
admin.site.register(Weather,WeatherAdmin)
admin.site.register(NewsCategory)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(AdsCategory, AdsCategoryAdmin)
admin.site.register(AdvertisementType, AdvertisementTypeAdmin)
admin.site.register(CreateAds, CreateAdsAdmin)