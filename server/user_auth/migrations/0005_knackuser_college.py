# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_auto_20150817_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackuser',
            name='college',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
