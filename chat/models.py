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
    ip = models.CharField(max_length=124, blank=True, null=True)
    gen = models.CharField(max_length=123, choices=GEN, blank=True, null=True)
    choose_gen = models.CharField(max_length=123, choices=GEN, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    years = models.ForeignKey(Years, on_delete=models.CASCADE, related_name='years', blank=True, null=True)
    choose_years = models.ForeignKey(Years, on_delete=models.CASCADE, related_name='choose_years', blank=True, null=True)


class Chat(models.Model):
    chat_name = models.CharField(max_length=123)
    create = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create')
    create2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create2')


class Massage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    massage = models.TextField()


class Apartment(models.Model):
    file = models.FileField(upload_to='file')
