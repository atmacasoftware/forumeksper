from django.urls import path
from mainpage.views import *

urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('hava-durumu/<weather_id>/', weather_page, name='weather_page'),
    path('haberler/genel/tum-haberler/', news, name='news'),
    path('haberler/<slug>/', category_news, name='category_news'),
]
