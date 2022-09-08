from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from mainpage.forms import WeatherForm
from mainpage.models import Citys, Weather, NewsCategory
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