from django.urls import path
from server.views import *

urlpatterns = [
    path('', rooms, name="rooms"),
    path('<slug:slug>/', room, name='room'),
    path('kesfet', room_find, name='room_find'),
]
