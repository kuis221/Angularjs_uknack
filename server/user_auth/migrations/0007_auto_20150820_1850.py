# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0006_auto_20150820_1808'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='knackuser',
            managers=[
                ('objects', user_auth.models.CustomUserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='college',
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='location',
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='staff_picked',
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='knackuser',
            name='email',
            field=models.EmailField(verbose_name='email address', max_length=254, unique=True),
        ),
    ]
