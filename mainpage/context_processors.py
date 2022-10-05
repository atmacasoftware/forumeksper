from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from mainpage.forms import WeatherForm
from mainpage.models import Citys, Weather, NewsCategory, CreateAds
import requests
import math

def weather(request):
    cities = Weather.objects.all().last()

    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=37a3b97ba41dfc38e67661578a88798d"

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])

    form = WeatherForm()
    weather_data = []

    city_weather = requests.get(url.format(cities)).json()

    weather = {
        'city': cities,
        'temparature': math.floor(city_weather['main']['temp'] - 273),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'humidity': city_weather['main']['humidity'],
        'pressure': city_weather['main']['pressure'],
        'windspeed': city_weather['wind']['speed']
    }

    #for city in cities:
    #    city_weather = requests.get(url.format(city)).json()
#
    #    weather = {
    #        'city':city,
    #        'temparature': math.floor(city_weather['main']['temp'] - 273),
    #        'description': city_weather['weather'][0]['description'],
    #        'icon': city_weather['weather'][0]['icon'],
    #        'humidity': city_weather['main']['humidity'],
    #        'pressure':city_weather['main']['pressure'],
    #        'windspeed': city_weather['wind']['speed']
    #    }
    #    weather_data.append(weather)
    context = {'weather':weather,'form':form}

    return context


def news_category(request):
    links = NewsCategory.objects.all().order_by('id')
    links_four = NewsCategory.objects.all().order_by('id')[:4]
    return dict(news_links=links, links_four=links_four)

def first_category_ads(request):
    ads = CreateAds.objects.filter(category__name="1. Kategori")
    return dict(firstcategoryads=ads)

def second_category_ads(request):
    ads1 = None
    ads2 = None
    ads3 = None

    ads = CreateAds.objects.filter(category__name="2. Kategori").count()

    if ads > 11 and ads < 21:

        try:
            ads1 = CreateAds.objects.filter(category__name="2. Kategori")[:10]
        except:
            ads1 = CreateAds.objects.filter(category__name="2. Kategori")

        try:
            ads2 = CreateAds.objects.filter(category__name="2. Kategori")[11:20]
        except:
            ads2 = CreateAds.objects.filter(category__name="2. Kategori")

    elif ads > 20:
        try:
            ads1 = CreateAds.objects.filter(category__name="2. Kategori")[:10]
        except:
            ads1 = CreateAds.objects.filter(category__name="2. Kategori")

        try:
            ads2 = CreateAds.objects.filter(category__name="2. Kategori")[11:20]
        except:
            ads2 = CreateAds.objects.filter(category__name="2. Kategori")

        try:
            ads3 = CreateAds.objects.filter(category__name="2. Kategori")[21:30]
        except:
            ads3 = CreateAds.objects.filter(category__name="2. Kategori")

    else:
        ads1 = CreateAds.objects.filter(category__name="2. Kategori")
        return dict(ads_count=ads, ads1=ads1, ads2=ads2, ads3=ads3)
    return dict(ads_count=ads, ads1=ads1, ads2=ads2, ads3=ads3)