import ast
import six
from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from rest_framework.authtoken.models import Token


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return six.text_type(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given user email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, last_seen=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class KnackUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Trans', 'Trans'),
        ('Andro', 'Andro'),
        ('Exploring', 'Exploring'),
        ('Alien', 'Alien'),
        ('No Gender', 'No Gender'),
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    username = models.CharField(_('username'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    notification_email = models.EmailField(_('email address for notifications'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    picture = models.ImageField(null=True, blank=True, upload_to='avatar/')
    gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER_CHOICES)
    age = models.SmallIntegerField(blank=True, null=True)
    college = models.ForeignKey('College', blank=True, null=True)
    year = models.ForeignKey('Year', blank=True, null=True)
    grand_total = models.FloatField(default=0.0, blank=False)

    about_me = models.TextField(null=False, blank=False, default='I\'m a senior here at Harvard University '
                                                                 'and study bio-engineering. I love writing '
                                                                 'and reading. Contact me anytime if you need help.')
    payment_venmo = models.CharField(max_length=255, blank=False, null=False, default='')
    payment_paypal = models.CharField(max_length=255, blank=False, null=False, default='')
    reasons = JSONField(default=['I\'m an awesome knacker',
                                 'Who absolutely loves what I do',
                                 'I\'m fun, fair and honest',
                                 'I\'ll do a great job everytime',
                                 'you\'ll really love your knack',
                                 ])

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(_('online status'), default=False)

    connections = models.ManyToManyField('self', related_name='connected_by', symmetrical=False, db_index=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    """
    @property
    def is_online(self):
        try:
            if (timezone.now() - self.last_seen).seconds / 60 < 30:
                return True
        except:
            return False
        return False
    """

    @property
    def full_name(self):
        return self.get_full_name()


class SocialLink(models.Model):
    user = models.OneToOneField(KnackUser)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    googleplus = models.CharField(max_length=255, blank=True)


@six.python_2_unicode_compatible
class Feedback(models.Model):
    user = models.ForeignKey(KnackUser)
    rating = models.SmallIntegerField()
    review = models.CharField(max_length=128, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user


class Description(models.Model):
    user = models.ForeignKey(KnackUser)
    description = models.CharField(max_length=255, blank=True)


@six.python_2_unicode_compatible
class College(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class Year(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class RegisterEmail(models.Model):
    uuid = models.CharField(max_length=64)
    email = models.EmailField()

    def __str__(self):
        return self.email


@receiver(post_save, sender=KnackUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
        instance.save()
