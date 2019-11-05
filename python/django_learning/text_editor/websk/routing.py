from django.urls import path

from websk.consumers import webConsumer

websocket_urlpatterns  = [
    path('webcs/', webConsumer),
]
