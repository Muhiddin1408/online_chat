from django.urls import path
from .views import register, SearchUser, chat_list, create_chat, massage_list, send_message, YearView, chat_delete, \
    last_login, massage_read, online, writing, writingid, file, delete_chat, html

urlpatterns = [
    path('register', register),
    path('online', online),
    path('search/', SearchUser.as_view()),
    path('year/', YearView.as_view()),
    path('chat/list/', chat_list),
    path('chat/delete/<int:pk>', chat_delete),
    path('delete/free/chat/<int:pk>', delete_chat),
    path('massage/read/<int:pk>', massage_read),
    path('create/chat/', create_chat),
    path('massage/list/<int:pk>', massage_list),
    path('login/time/', last_login),
    path('send/message/', send_message),
    path('writing/', writing),
    path('file/', file),
    path('writing/<int:pk>', writingid),
    path('html', html),
]
