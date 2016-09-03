from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'sender', 'type', 'is_read', 'created_at')

