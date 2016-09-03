# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0017_registeremail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='gender',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'MM', b'Male'), (b'FF', b'Female'), (b'TT', b'Transgender'), (b'II', b'Intersex'), (b'GN', b'Gender Neutral'), (b'GQ', b'Genderqueer'), (b'CC', b'Cisgender'), (b'BB', b'Bigender'), (b'PP', b'Pangender')]),
        ),
    ]
