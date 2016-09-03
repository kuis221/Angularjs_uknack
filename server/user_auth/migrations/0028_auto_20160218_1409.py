# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0027_auto_20160212_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='knackuser',
            name='age',
            field=models.SmallIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='year',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
