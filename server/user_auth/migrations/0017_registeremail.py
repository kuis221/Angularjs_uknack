# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0016_knackuser_last_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
