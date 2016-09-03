import uuid
import os
import shutil

import six
import png
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from redactor.fields import RedactorField

User = settings.AUTH_USER_MODEL

KNACK_IDEA_TYPES = (
    ('O', 'Offered'),
)


class KnackManager(models.Manager):
    def get_queryset(self):
        return super(KnackManager, self).get_queryset().filter(deleted=False).order_by('-created_at')


@six.python_2_unicode_compatible
class Knack(models.Model):
    anonymous = models.BooleanField(default=False, null=False, blank=False)
    username = models.CharField('Anonymous Username', max_length=255, default='', null=True, blank=True)

    name = models.CharField('Knack headline', max_length=100, null=False, blank=False)
    description = models.TextField('Tell us more about what you do', null=True, blank=True)
    category = models.ForeignKey('Category', null=False, blank=False, verbose_name='Knack category')
    price = models.FloatField('What is your rate?', default=0.0, blank=False)
    KNACK_TYPES = (
        ('O', 'Offered'),
        ('W', 'Wanted'),
    )
    type = models.CharField(max_length=1, choices=KNACK_TYPES, null=False, blank=False, default='O')
    schedule = models.CharField('What\'s your schedule like?', max_length=255, null=True, blank=True)

    travel_choices = ((True, 'Yes'), (False, 'No'))
    willing_to_travel = models.BooleanField('Are you willing to travel?', choices=travel_choices, default=True)
    miles_choices = (('5 miles', '5 miles'), ('10 miles', '10 miles'), ('20 miles', '20 miles'),
                     ('50+ miles', '50+ miles'), ('On Campus', 'On Campus'))
    miles = models.CharField('How many miles?', max_length=255, choices=miles_choices, default='On Campus')

    charge_choices = (('Flat Fee', 'Flat Fee'), ('Hourly', 'Hourly'))
    how_charge = models.CharField('How do you charge?', max_length=255, choices=charge_choices, default='Hourly')

    photo0 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo1 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo2 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo3 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    photo4 = models.ImageField(null=True, blank=True, upload_to='knacks/')
    video = models.ImageField(upload_to='knacks/videos/', null=True, blank=True)

    owner = models.ForeignKey(User, null=False, blank=False, related_name='knacks')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    views = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)

    # Retrieve only not deleted items
    objects = KnackManager()

    def delete(self, *args, **kwargs):
        # We do not delete anything. See also:
        # https://docs.djangoproject.com/en/1.9/topics/db/models/#overriding-model-methods
        self.deleted = True
        self.save()
        return True

    def __str__(self):
        return '%s' % (self.name, )


def image_handler(instance, **kwargs):
    for i in range(5):
        photo = getattr(instance, 'photo%s' % i, None)
        if photo:
            try:
                reader = png.Reader(filename=photo.path)
                width, height, data, opts = reader.read()
                if opts['interlace'] == 0:
                    opts['interlace'] = 1
                    tmp_file = os.path.join('/tmp', str(uuid.uuid4()))
                    writer = png.Writer(width, height, **opts)
                    with open(tmp_file, 'wb') as file:
                        writer.write(file, data)
                    shutil.move(tmp_file, photo.path)
            except Exception as e:
                print('Exception on image interlacing', e)

post_save.connect(image_handler, sender=Knack)


@six.python_2_unicode_compatible
class KnackIdea(models.Model):
    name = models.CharField('Knack headline', max_length=255, null=False, blank=False)
    description = models.TextField('Tell us more about what you do', null=True, blank=True)
    category = models.ForeignKey('Category', null=False, blank=False, verbose_name='Knack category')
    type = models.CharField(max_length=1, choices=KNACK_IDEA_TYPES, null=False, blank=False, default='O')
    schedule = models.CharField('What\'s your schedule like?', max_length=255, null=True, blank=True)

    travel_choices = ((True, 'Yes'), (False, 'No'))
    willing_to_travel = models.BooleanField('Are you willing to travel?', choices=travel_choices, default=True)
    miles_choices = (('5 miles', '5 miles'), ('10 miles', '10 miles'), ('20 miles', '20 miles'),
                     ('50+ miles', '50+ miles'), ('On Campus', 'On Campus'))
    miles = models.CharField('How many miles?', max_length=255, choices=miles_choices, default='On Campus')
    price = models.FloatField('What is your rate?', default=0.0)
    charge_choices = (('Flat Fee', 'Flat Fee'), ('Hourly', 'Hourly'))
    how_charge = models.CharField('How do you charge?', max_length=255, choices=charge_choices, default='Hourly')
    business_model = RedactorField(verbose_name='Business Model', allow_file_upload=True,
                                   allow_image_upload=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.name


class KnackIdeaImage(models.Model):
    knack_idea = models.ForeignKey(KnackIdea)
    photo = models.ImageField(upload_to='knacks/images/', null=True, blank=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().order_by('name')


@six.python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
