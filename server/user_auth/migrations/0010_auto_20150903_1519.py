# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0009_auto_20150902_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='age',
            field=models.IntegerField(blank=True, default=20, max_length=2),
        ),
    ]
