from django.urls import path
from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notification/', NotificationConsumer.as_asgi()),
]