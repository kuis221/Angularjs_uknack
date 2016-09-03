# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0003_knack_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knack',
            name='owner',
            field=models.ForeignKey(related_name='knacks', to=settings.AUTH_USER_MODEL),
        ),
    ]
