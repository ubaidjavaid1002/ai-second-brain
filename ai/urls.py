from django.urls import path

from .views import (
    chat_page,
    chat_api,
    new_chat,
    delete_chat
)

urlpatterns = [
    path('', chat_page, name='chat'),

    path('new/', new_chat, name='new_chat'),

    path('send/', chat_api, name='chat_api'),

    path(
        '<int:conversation_id>/',
        chat_page,
        name='conversation_detail'
    ),

    path(
        '<int:conversation_id>/delete/',
        delete_chat,
        name='delete_chat'
    ),
]