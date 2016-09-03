# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0015_auto_20150915_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackuser',
            name='last_seen',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
