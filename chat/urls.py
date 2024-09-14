from django.urls import path
from .views import (
    YearView, SearchUser, getMe, register, chat_list, create_chat, massage_list, send_message,
    chat_delete, last_login, massage_read, online, writing, writingid,
    file, delete_chat, html, report_themes, report_user)

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
    path('privacy', html),
    path('report_theme/list/', report_themes),
    path('report/user', report_user),
    path('me/', getMe)
]
