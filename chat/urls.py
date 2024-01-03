from django.urls import path
from .views import register, SearchUser, chat_list, create_chat, massage_list, send_message, YearView, chat_delete

urlpatterns = [
    path('register', register),
    path('search/', SearchUser.as_view()),
    path('year/', YearView.as_view()),
    path('chat/list/', chat_list),
    path('chat/delete/<int:pk>', chat_delete),
    path('create/chat/', create_chat),
    path('massage/list/<int:pk>', massage_list),
    path('send/message/', send_message),
]