from django.urls import path
from gaming.views import *

urlpatterns = [
    path('', game_mainpage, name='game_mainpage')
]