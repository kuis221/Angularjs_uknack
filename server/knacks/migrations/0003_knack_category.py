# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0002_auto_20150818_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='knack',
            name='category',
            field=models.ForeignKey(default=1, to='knacks.Category'),
            preserve_default=False,
        ),
    ]
