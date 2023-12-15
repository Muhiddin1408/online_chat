from django.urls import path
from .views import register, SearchUser, chat_list

urlpatterns = [
    path('', register),
    path('get/', SearchUser.as_view()),
    path('chat_list/', chat_list),
]