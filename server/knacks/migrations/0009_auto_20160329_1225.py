# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0008_auto_20160229_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='knack',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='knack',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
