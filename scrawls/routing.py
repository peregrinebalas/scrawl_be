from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(r'^ws/walls/<int:pk>', ChatConsumer)
]
