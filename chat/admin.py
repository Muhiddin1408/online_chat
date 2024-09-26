from django.contrib import admin

from chat.models import (
    User, Chat, Years, Massage, Apartment, Privacy,
    ReportTheme, UserReport, UserBlock, RestrictedWord)
from django.db import IntegrityError

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'username', 'email', 'first_name', 'last_name', 'ip')
    search_fields = ('id', 'username', 'ip')
    actions = ['ban_selected_users']

    def ban_selected_users(self, request, queryset):
        for user in queryset:
            # Create or update UserBlock entry for the user
            reporter = User.objects.get(is_superuser=True)
            try:
                user_block, created = UserBlock.objects.get_or_create(user=user, blocked_by=reporter)
                user_block.ban_user(hours=24, reason="Banned by admin", banned_by=request.user)
            except IntegrityError as e:
                user_block = UserBlock.objects.get(user=user)
                user_block.ban_user(hours=24, reason="Banned by admin", banned_by=request.user)
        self.message_user(request, "Selected users have been banned.")
    ban_selected_users.short_description = "Ban selected users"


class UserReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reporter', 'theme', 'chat', 'reason', 'created_at')
    list_filter = ('theme', 'created_at')


class MessageModelInline(admin.TabularInline):
    model = Massage
    extra = 1

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sender', 'receiver', 'free', 'updated_at')
    list_filter = ('free', 'updated_at')
    search_fields = ('id', 'name')
    inlines = [MessageModelInline]



admin.site.register(Years)
admin.site.register(Massage)
admin.site.register(Apartment)
admin.site.register(Privacy)
admin.site.register(ReportTheme)
admin.site.register(UserBlock)
admin.site.register(RestrictedWord)
admin.site.register(User, UserAdmin)
admin.site.register(UserReport, UserReportAdmin)
admin.site.register(Chat, ChatAdmin)