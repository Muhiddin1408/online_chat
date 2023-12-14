from django.urls import path
from .views import register, SearchUser

urlpatterns = [
    path('', register),
    path('get/', SearchUser.as_view()),
]