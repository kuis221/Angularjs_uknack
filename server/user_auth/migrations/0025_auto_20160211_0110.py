# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0024_auto_20160208_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knackuser',
            name='reason',
        ),
        migrations.AddField(
            model_name='reason',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
