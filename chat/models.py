import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from general.models import BaseModel
# Create your models here.


class Years(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"


class User(AbstractUser):

    GENDER = (
        ('man', "MAN"),
        ('woman', "WOMAN"),
        ('all', "ALL"),
    )
    LANGUAGE = (
        ('uz', "UZ"),
        ('ru', "RU"),
        ('en', "EN"),
    )
    uuid = models.UUIDField(    
        unique=True,
        default = uuid.uuid4, 
        editable = False)
    username = models.CharField(max_length=24, unique=False, null=True, blank=True)
    ip = models.CharField(max_length=124, blank=True, null=True)
    gender = models.CharField(max_length=123, choices=GENDER, blank=True, null=True)
    target_gender = models.CharField(max_length=123, choices=GENDER, blank=True, null=True)
    language = models.CharField(max_length=123, choices=LANGUAGE, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    years = models.ForeignKey(Years, on_delete=models.CASCADE, related_name='years', blank=True, null=True)
    target_years = models.ManyToManyField(Years, related_name='choose_years')
    writing = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.ip if self.ip else str(self.id)


class Chat(models.Model):
    name = models.CharField(max_length=123)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',
                               blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver',
                                 blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=True)
    free = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"ID: {self.id}"



class Massage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.chat} | {self.user} | {self.message} | {self.is_read}"


class Apartment(models.Model):
    file = models.FileField(upload_to='file')


class Privacy(models.Model):
    text = models.TextField()


class ReportTheme(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    point = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Report Theme"
        verbose_name_plural = "Report Themes"


class UserReport(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="declarations")
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    theme = models.ForeignKey(ReportTheme, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "User Report"
        verbose_name_plural = "User Reports"

    def __str__(self):
        return f"👤: {self.user} | 🚫: {self.reporter} | 🟨{self.theme} | 💬{self.reason} | 🕒{self.created_at}"


class UserBlock(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='block')
    blocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    blocked_until = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        if self.blocked_until and timezone.now() < self.blocked_until:
            return True
        return False

    def ban_user(self, hours=24, reason=None, banned_by=None):
        self.blocked_until = timezone.now() + timedelta(hours=hours)
        if reason:
            self.reason = reason
        if banned_by:
            self.banned_by = banned_by
        self.save()

    def revoke_ban(self):
        self.blocked_until = None
        self.save()

    def __str__(self):
        return f'User: {self.user.username} banned until {self.blocked_until + timedelta(hours=5)}'

    class Meta:
        verbose_name = 'Blocked User'
        verbose_name_plural = 'Blocked Users'
        ordering = ['-created_at']


class RestrictedWord(BaseModel):
    title = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Restricted Word'
        verbose_name_plural = 'Restricted Words'