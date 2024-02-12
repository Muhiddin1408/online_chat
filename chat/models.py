from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Years(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()


class User(AbstractUser):

    GEN = (
        ('man', "MAN"),
        ('woman', "WOMAN"),
        ('all', "ALL"),
    )
    LANG = (
        ('uz', "UZ"),
        ('ru', "RU"),
        ('en', "EN"),
    )
    ip = models.CharField(max_length=124, blank=True, null=True)
    gen = models.CharField(max_length=123, choices=GEN, blank=True, null=True)
    lang = models.CharField(max_length=123, choices=LANG, blank=True, null=True)
    choose_gen = models.CharField(max_length=123, choices=GEN, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    years = models.ForeignKey(Years, on_delete=models.CASCADE, related_name='years', blank=True, null=True)
    choose_years = models.ManyToManyField(Years, related_name='choose_years', blank=True, null=True)
    writing = models.BooleanField(default=False)


class Chat(models.Model):
    chat_name = models.CharField(max_length=123)
    create = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create')
    create2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create2')
    updated_at = models.DateTimeField(blank=True, null=True)
    deletes = models.BooleanField(default=True)


class Massage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    massage = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    read = models.BooleanField(default=False)


class Apartment(models.Model):
    file = models.FileField(upload_to='file')
