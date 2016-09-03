# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0011_auto_20150903_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('twitter', models.CharField(max_length=255, blank=True, null=True)),
                ('facebook', models.CharField(max_length=255, blank=True, null=True)),
                ('instagram', models.CharField(max_length=255, blank=True, null=True)),
                ('googleplus', models.CharField(max_length=255, blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
