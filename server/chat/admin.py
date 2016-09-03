from django.contrib import admin

from chat import models


@admin.register(models.Message)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sender', 'receipt', 'is_read', 'created_at', 'body')
