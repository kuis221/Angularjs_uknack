# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_knackuser_college'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='picture',
            field=models.ImageField(upload_to='avatar', null=True, blank=True),
        ),
    ]
