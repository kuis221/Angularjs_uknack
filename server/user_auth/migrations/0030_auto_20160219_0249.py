# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0029_auto_20160218_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='picture',
            field=models.ImageField(max_length=255, null=True, upload_to=b'avatar', blank=True),
        ),
    ]
