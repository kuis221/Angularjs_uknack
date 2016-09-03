# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0025_auto_20160211_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reason',
            name='user',
        ),
        migrations.AddField(
            model_name='knackuser',
            name='reasons',
            field=user_auth.models.ListField(default=[b"I'm an awesome knacker", b'Who absolutely loves what I do', b"I'm fun, fair and honest", b"I'll do a great job everytime", b"you'll really love your knack"]),
        ),
        migrations.DeleteModel(
            name='Reason',
        ),
    ]
