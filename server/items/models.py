import six
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from knacks.models import image_handler

User = settings.AUTH_USER_MODEL

ITEM_TYPES = (
    ('O', 'Offered'),
    ('W', 'Wanted'),
)


class ItemManager(models.Manager):
    def get_queryset(self):
        return super(ItemManager, self).get_queryset().filter(deleted=False).order_by('-created_at')


@six.python_2_unicode_compatible
class Item(models.Model):
    anonymous = models.BooleanField(default=False, null=False, blank=False)
    username = models.CharField('Anonymous Username', max_length=255, default='', null=True, blank=True)

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', null=False, blank=False)
    price = models.FloatField(default=0.0, blank=False)
    type = models.CharField(max_length=1, choices=ITEM_TYPES, null=False, blank=False)

    photo0 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo1 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo2 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo3 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo4 = models.ImageField(null=True, blank=True, upload_to='knacks/')

    schedule = models.CharField('What\'s your schedule like?', max_length=255, null=True, blank=True)
    miles_choices = (('5 miles', '5 miles'), ('10 miles', '10 miles'), ('20 miles', '20 miles'),
                     ('50+ miles', '50+ miles'), ('On Campus', 'On Campus'))
    miles = models.CharField('How far?', max_length=255, choices=miles_choices, default='On Campus')

    travel_choices = ((True, 'Yes'), (False, 'No'))
    willing_to_travel = models.BooleanField('Are you willing to travel?', choices=travel_choices, default=True)

    owner = models.ForeignKey(User, null=False, blank=False, related_name='items')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    views = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)

    # Retrieve only not deleted items
    objects = ItemManager()

    def delete(self, *args, **kwargs):
        # We do not delete anything. See also:
        # https://docs.djangoproject.com/en/1.9/topics/db/models/#overriding-model-methods
        self.deleted = True
        self.save()
        return True

    def __str__(self):
        return '%s\'s %s' % (self.owner, self.name)


post_save.connect(image_handler, sender=Item)


@six.python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
