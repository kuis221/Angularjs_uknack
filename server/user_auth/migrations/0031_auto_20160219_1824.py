# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0030_auto_20160219_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='about_me',
            field=models.TextField(default=b"I'm a senior here at Harvard University and study bio-engineering. I love writing and reading. Contact me anytime if you need help."),
        ),
    ]
