# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_remove_knackuser_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='gender',
            field=models.CharField(max_length=2, choices=[('MM', 'Male'), ('FF', 'Female'), ('TT', 'Transgender'), ('II', 'Intersex'), ('GN', 'Gender Neutral'), ('GQ', 'Genderqueer'), ('CC', 'Cisgender'), ('BB', 'Bigender'), ('PP', 'Pangender')]),
        ),
    ]
