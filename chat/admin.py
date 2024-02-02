from django.contrib import admin

from chat.models import User, Chat, Years, Massage, Apartment

# Register your models here.


admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Years)
admin.site.register(Massage)
admin.site.register(Apartment)
