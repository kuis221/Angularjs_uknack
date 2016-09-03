# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0008_auto_20150820_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knackuser',
            name='birthday',
        ),
        migrations.AddField(
            model_name='knackuser',
            name='age',
            field=models.IntegerField(blank=True, default=0, max_length=2),
        ),
    ]
