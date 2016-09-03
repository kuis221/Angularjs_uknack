# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20150917_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='item',
            name='video',
        ),
        migrations.AddField(
            model_name='item',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='miles',
            field=models.CharField(default=b'On Campus', max_length=255, verbose_name=b'How far?', choices=[(b'5 miles', b'5 miles'), (b'10 miles', b'10 miles'), (b'20 miles', b'20 miles'), (b'50+ miles', b'50+ miles'), (b'On Campus', b'On Campus')]),
        ),
        migrations.AddField(
            model_name='item',
            name='photo0',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='photo1',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='photo2',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='photo3',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='photo4',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='schedule',
            field=models.CharField(max_length=255, null=True, verbose_name=b"What's your schedule like?", blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='username',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Anonymous Username', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='willing_to_travel',
            field=models.BooleanField(default=True, verbose_name=b'Are you willing to travel?', choices=[(True, b'Yes'), (False, b'No')]),
        ),
    ]
