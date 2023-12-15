from django.urls import path
from .views import register, SearchUser, chat_list, create_chat, massage_list, send_message

urlpatterns = [
    path('register', register),
    path('search/', SearchUser.as_view()),
    path('chat/list/', chat_list),
    path('create/chat/', create_chat),
    path('massage/list/', massage_list),
    path('send/message/', send_message),
]