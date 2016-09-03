# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0012_sociallink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='age',
            field=models.SmallIntegerField(blank=True, default=20),
        ),
    ]
