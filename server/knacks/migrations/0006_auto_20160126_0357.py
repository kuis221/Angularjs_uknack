# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0005_knackidea_knackideaimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knack',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='knackidea',
            name='miles',
            field=models.CharField(default=b'On Campus', max_length=255, verbose_name=b'How many miles?', choices=[(b'5 miles', b'5 miles'), (b'10 miles', b'10 miles'), (b'20 miles', b'20 miles'), (b'50+ miles', b'50+ miles'), (b'On Campus', b'On Campus')]),
        ),
        migrations.AlterField(
            model_name='knackidea',
            name='rate',
            field=models.FloatField(default=0.0, verbose_name=b'What is your rate?'),
        ),
    ]
