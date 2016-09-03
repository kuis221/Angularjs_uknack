# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0007_knackidea_business_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knack',
            name='photo',
        ),
        migrations.AddField(
            model_name='knack',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='knack',
            name='how_charge',
            field=models.CharField(default=b'Hourly', max_length=255, verbose_name=b'How do you charge?', choices=[(b'Flat Fee', b'Flat Fee'), (b'Hourly', b'Hourly')]),
        ),
        migrations.AddField(
            model_name='knack',
            name='miles',
            field=models.CharField(default=b'On Campus', max_length=255, verbose_name=b'How many miles?', choices=[(b'5 miles', b'5 miles'), (b'10 miles', b'10 miles'), (b'20 miles', b'20 miles'), (b'50+ miles', b'50+ miles'), (b'On Campus', b'On Campus')]),
        ),
        migrations.AddField(
            model_name='knack',
            name='photo0',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='photo1',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='photo2',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='photo3',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='photo4',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='schedule',
            field=models.CharField(max_length=255, null=True, verbose_name=b"What's your schedule like?", blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='username',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Anonymous Username', blank=True),
        ),
        migrations.AddField(
            model_name='knack',
            name='willing_to_travel',
            field=models.BooleanField(default=True, verbose_name=b'Are you willing to travel?', choices=[(True, b'Yes'), (False, b'No')]),
        ),
        migrations.AlterField(
            model_name='knack',
            name='category',
            field=models.ForeignKey(verbose_name=b'Knack category', to='knacks.Category'),
        ),
        migrations.AlterField(
            model_name='knack',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Tell us more about what you do', blank=True),
        ),
        migrations.AlterField(
            model_name='knack',
            name='name',
            field=models.CharField(max_length=100, verbose_name=b'Knack headline'),
        ),
        migrations.AlterField(
            model_name='knack',
            name='price',
            field=models.FloatField(default=0.0, verbose_name=b'What is your rate?'),
        ),
        migrations.AlterField(
            model_name='knack',
            name='type',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'O', b'Offered'), (b'W', b'Wanted')]),
        ),
    ]
