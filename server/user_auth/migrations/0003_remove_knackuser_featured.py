# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_knackuser_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knackuser',
            name='featured',
        ),
    ]
