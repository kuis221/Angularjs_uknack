# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20160321_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
