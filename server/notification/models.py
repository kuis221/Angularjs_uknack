import six
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

User = settings.AUTH_USER_MODEL


class NotificationManager(models.Manager):
    def get_queryset(self):
        return super(NotificationManager, self).get_queryset().order_by('-created_at')

    def unread(self):
        return self.filter(is_read=False)


@six.python_2_unicode_compatible
class Notification(models.Model):
    TYPE_KNACK_OFFERED = 'KO'
    TYPE_KNACK_WANTED = 'KW'
    TYPE_ITEM_OFFERED = 'IO'
    TYPE_ITEM_WANTED = 'IW'
    TYPE_CONNECTION = 'CN'
    TYPES = (
        (TYPE_KNACK_OFFERED, 'Knack offered'),
        (TYPE_KNACK_WANTED, 'Knack wanted'),
        (TYPE_ITEM_OFFERED, 'Item offered'),
        (TYPE_ITEM_WANTED, 'Item wanted'),
        (TYPE_CONNECTION, 'Connection'),
    )

    user = models.ForeignKey(User, related_name='notifications')
    sender = models.ForeignKey(User, related_name='+')
    type = models.CharField(max_length=2, choices=TYPES)
    data = JSONField(blank=True, default={})
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = NotificationManager()

    def __str__(self):
        return 'Notification'
