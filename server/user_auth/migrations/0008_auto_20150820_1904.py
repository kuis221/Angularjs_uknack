# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_auto_20150820_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackuser',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='college',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='gender',
            field=models.CharField(choices=[('MM', 'Male'), ('FF', 'Female'), ('TT', 'Transgender'), ('II', 'Intersex'), ('GN', 'Gender Neutral'), ('GQ', 'Genderqueer'), ('CC', 'Cisgender'), ('BB', 'Bigender'), ('PP', 'Pangender')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='picture',
            field=models.ImageField(blank=True, upload_to='avatar', null=True),
        ),
    ]
