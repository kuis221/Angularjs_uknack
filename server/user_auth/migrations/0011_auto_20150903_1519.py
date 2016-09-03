# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_auto_20150903_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='age',
            field=models.SmallIntegerField(blank=True, max_length=2, default=20),
        ),
    ]
