from django.urls import path
from server.views import *

urlpatterns = [
    path('', rooms, name="rooms"),
    path('<slug:slug>/', room, name='room'),
    path('json/<slug:slug>/', json_room_message, name='json_room_message'),
    path('kesfet', room_find, name='room_find'),
]
