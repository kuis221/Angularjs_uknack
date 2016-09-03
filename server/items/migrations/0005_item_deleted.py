# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_item_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
