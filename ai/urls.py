from django.urls import path
from .views import chat_page, chat_api

urlpatterns = [
    path('', chat_page, name='chat'),
    path('send/', chat_api, name='chat_api'),
]