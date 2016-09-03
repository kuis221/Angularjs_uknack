# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0021_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackuser',
            name='reason',
            field=models.ManyToManyField(to='user_auth.Reason', null=True, blank=True),
        ),
    ]
