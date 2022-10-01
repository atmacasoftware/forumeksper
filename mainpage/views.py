import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from mainpage.forms import WeatherForm
from forums.models import Forum
from mainpage.models import LoanInterestRate, Weather, NewsCategory, Note, Advertisement, AdsCategory, AdvertisementType
# Create your views here.
from notifications.models import Notification
from user_account.models import UserProfile
import datetime
import math
import http.client


def mainpage(request):
    profile = UserProfile.objects.all()
    person_profile = None
    notification = None
    notification_count = None
    notification_unread = None
    popular_forums = None

    try:
        popular_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')[:10]
    except:
        popular_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')

    bank_rate_list = LoanInterestRate.objects.filter(bank__is_important=True).order_by('bank__name')

    if request.user.is_authenticated:
        person_profile = UserProfile.objects.get(user=request.user)
        notification = Notification.objects.filter(recipient_user=request.user).order_by('-created_at')
        notification_count = Notification.objects.filter(recipient_user=request.user).count()

    ip = request.META['REMOTE_ADDR']
    cities = Weather.objects.filter(ip=ip).last()

    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=37a3b97ba41dfc38e67661578a88798d"

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ip = ip
            data.save()
            return redirect(request.META['HTTP_REFERER'])

    form = WeatherForm()
    weather_data = []

    city_weather = requests.get(url.format(cities)).json()

    weather = {
        'city': cities,
        'temparature': round(city_weather['main']['temp'] - 273.15, 1),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'humidity': city_weather['main']['humidity'],
        'pressure': city_weather['main']['pressure'],
        'windspeed': city_weather['wind']['speed']
    }

    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 0su0rS8l9QBSmEq2Y7UVeh:3jpAYiOzccBwtzpyZGlxCQ"
    }
    conn.request("GET", "/news/getNews?country=tr&tag=general", headers=headers)
    res = conn.getresponse()
    data = res.read()
    news = data.decode("utf-8")
    response = requests.request("GET", "https://api.collectapi.com/news/getNews?country=tr&tag=general",
                                headers=headers)
    new = response.json()

    # print(new["result"])

    mainpage_news = new["result"]

    context = {
        'profile': profile,
        'person_profile': person_profile,
        'notification': notification,
        'notification_count': notification_count,
        'notification_unread': notification_unread,
        'popular_forums': popular_forums,
        'bank_rate_list': bank_rate_list,
        'weather': weather,
        'form': form,
        'news': news,
        'mainpage_news': mainpage_news
    }

    return render(request, 'pages/mainpage.html', context)


def weather_page(request, weather_id):
    ip = request.META['REMOTE_ADDR']
    city = Weather.objects.get(ip=ip, id=weather_id)

    api = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=37a3b97ba41dfc38e67661578a88798d"
    city_weather = requests.get(api.format(city)).json()
    weather = {
        'city': city,
        'temparature': round((city_weather['main']['temp'] - 273.15), 1),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'humidity': city_weather['main']['humidity'],
        'pressure': city_weather['main']['pressure'],
        'windspeed': city_weather['wind']['speed'],
        'feels_like': round((city_weather['main']['feels_like'] - 273.15), 1),
        'winddegree': city_weather['wind']['deg'],
    }

    context = {
        'weather': weather,
        'city': city
    }

    return render(request, 'pages/weather.html', context)


def news(request):
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 0su0rS8l9QBSmEq2Y7UVeh:3jpAYiOzccBwtzpyZGlxCQ"
    }

    response = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag=general",
                                headers=headers)
    news = response.json()
    news_result = news["result"]

    slider = news_result[:7]

    ##Kategoriler
    response_economy = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag=economy",
                                        headers=headers)
    news_economy = response_economy.json()
    economy_news = news_economy["result"]

    response_technology = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag=technology",
                                           headers=headers)
    news_technology = response_technology.json()
    technology_news = news_technology["result"]

    response_sport = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag=sport",
                                      headers=headers)
    news_sport = response_sport.json()
    sport_news = news_sport["result"]

    response_health = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag=health",
                                       headers=headers)
    news_health = response_health.json()
    health_news = news_health["result"]

    response_world = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag=world",
                                      headers=headers)
    news_world = response_world.json()
    world_news = news_world["result"]

    response_entertainment = requests.request("GET",
                                              f"https://api.collectapi.com/news/getNews?country=tr&tag=entertainment",
                                              headers=headers)
    news_entertainment = response_entertainment.json()
    entertainment_news = news_entertainment["result"]

    context = {
        'news_result': news_result,
        'slider': slider,
        'economy_news': economy_news,
        'technology': technology_news,
        'sport_news': sport_news,
        'health_news': health_news,
        'world_news': world_news,
        'entertainment_news': entertainment_news
    }

    return render(request, 'pages/haberler/main.html', context)


def category_news(request, slug):
    category = NewsCategory.objects.get(slug=slug)

    select_category = category.name

    if select_category == 'Genel':
        category = 'general'

    if select_category == 'Ekonomi':
        category = 'economy'

    if select_category == 'Spor':
        category = 'sport'

    if select_category == 'Dünya':
        category = 'world'

    if select_category == 'Teknoloji':
        category = 'technology'

    if select_category == 'Sağlık':
        category = 'health'

    if select_category == 'Eğlence & Sanat':
        category = 'entertainment'

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 0su0rS8l9QBSmEq2Y7UVeh:3jpAYiOzccBwtzpyZGlxCQ"
    }

    response = requests.request("GET", f"https://api.collectapi.com/news/getNews?country=tr&tag={category}",
                                headers=headers)
    news = response.json()
    category_news = news["result"]

    slider = category_news[:7]

    category_news_four = category_news[:4]

    context = {
        'category_news': category_news,
        'category': category,
        'slider': slider,
        'select_category': select_category,
        'category_news_four': category_news_four,
    }

    return render(request, 'pages/haberler/category.html', context)


def advertisement(request):
    notes = None
    categories = AdsCategory.objects.all()
    advertisement_types = AdvertisementType.objects.all()

    try:
        notes = Note.objects.filter(pages="2")
    except:
        notes = None

    if request.method == 'POST':
        try:
            postData = request.POST
            first_name = postData.get('first_name', '')
            last_name = postData.get('last_name', '')
            email = postData.get('email', '')
            phone = postData.get('phone', '')
            company_name = postData.get('company_name', '')
            ads_type = postData.get('ads_type', '')
            ads_category = postData.get('ads_category', '')
            title = postData.get('title', '')
            message = postData.get('message', '')
            private = postData.get('is_private', '')
            image = request.FILES.get("image")

            category = None
            type = None

            try:
                category = get_object_or_404(AdsCategory, slug=ads_category)
            except:
                category = None

            try:
                type = get_object_or_404(AdvertisementType, slug=ads_type)
            except:
                type = None

            if private == 'on':
                private = True
            else:
                private = False
            data = Advertisement.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                                company=company_name, type=type, ads=category, title=title,
                                                message=message, image=image, is_private=private)
            data.save()
            messages.success(request, 'İlanınız başarıyla gönderildi. Ekipimiz tarafından yapılan incelemlere göre yaklaşık 24 saat içerisinde sizlere ulaşacağız.')
            return redirect('advertisement')
        except:
            messages.info(request, 'İşaretli alanların doldurulması gerekmektedir.')

            return redirect('advertisement')
    pass

    context = {
        'notes': notes,
        'categories':categories,
        'advertisement_types':advertisement_types
    }

    return render(request, 'pages/ads/create_ads.html', context)


def ads_info(request):
    ads_type1 = AdsCategory.objects.filter(name="1. Kategori")
    ads_type2 = AdsCategory.objects.filter(name="2. Kategori")
    ads_type3 = AdsCategory.objects.filter(name="3. Kategori")
    ads_type4 = AdsCategory.objects.filter(name="4. Kategori")
    ads_type5 = AdsCategory.objects.filter(name="5. Kategori")

    context = {
        ads_type1: 'ads_type1',
        ads_type2: 'ads_type2',
        ads_type3: 'ads_type3',
        ads_type4: 'ads_type4',
        ads_type5: 'ads_type5'
    }

    return render(request,'pages/ads/info.html',context)

############# Error Pages ##############
def error_404(request, exception):
    return render(request, 'pages/error/404.html', status=404)


def error_500(request):
    return render(request, 'pages/error/500.html', status=500)
