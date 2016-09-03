import six
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class MessageManager(models.Manager):
    def get_queryset(self):
        return super(MessageManager, self).get_queryset().order_by('-created_at')


@six.python_2_unicode_compatible
class Message(models.Model):
    CREATED_AT_FORMAT = '%b %d / %I:%M %p'

    sender = models.ForeignKey(User, related_name='senders')
    receipt = models.ForeignKey(User, related_name='receipts')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return 'Message #%s' % self.pk
