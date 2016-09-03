# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackuser',
            name='gender',
            field=models.CharField(max_length=1, default='M', choices=[('M', 'Male'), ('F', 'Female')]),
            preserve_default=False,
        ),
    ]
