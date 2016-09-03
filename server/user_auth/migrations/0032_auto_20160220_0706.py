# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0031_auto_20160219_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='picture',
            field=models.TextField(null=True, blank=True),
        ),
    ]
