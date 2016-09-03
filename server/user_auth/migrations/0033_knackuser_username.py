# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0032_auto_20160220_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackuser',
            name='username',
            field=models.CharField(max_length=30, verbose_name='username', blank=True),
        ),
    ]
