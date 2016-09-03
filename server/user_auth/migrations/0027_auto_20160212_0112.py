# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0026_auto_20160212_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='last_seen',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
