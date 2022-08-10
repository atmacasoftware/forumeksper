from django.urls import re_path
from .consumer import *

websocket_urlpatterns = [
    re_path(r'ws/server/(?P<room_name>\w+)/$', ChatConsumer.as_asgi())
]