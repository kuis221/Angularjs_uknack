# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0004_auto_20150917_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnackIdea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Knack headline')),
                ('description', models.TextField(null=True, verbose_name=b'Tell us more about what you do', blank=True)),
                ('type', models.CharField(default=b'O', max_length=1, choices=[(b'O', b'Offered')])),
                ('schedule', models.CharField(max_length=255, null=True, verbose_name=b"What's your schedule like?", blank=True)),
                ('willing_to_travel', models.BooleanField(default=True, verbose_name=b'Are you willing to travel?', choices=[(True, b'Yes'), (False, b'No')])),
                ('miles', models.CharField(default=b'5 miles', max_length=255, verbose_name=b'How many miles?', choices=[(b'5 miles', b'5 miles'), (b'10 miles', b'10 miles'), (b'20 miles', b'20 miles'), (b'50+ miles', b'50+ miles')])),
                ('rate', models.IntegerField(default=0, verbose_name=b'What is your rate?')),
                ('how_charge', models.CharField(default=b'Hourly', max_length=255, verbose_name=b'How do you charge?', choices=[(b'Flat Fee', b'Flat Fee'), (b'Hourly', b'Hourly')])),
                ('created_at', models.DateField(auto_now_add=True)),
                ('modified_at', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(verbose_name=b'Knack category', to='knacks.Category')),
            ],
        ),
        migrations.CreateModel(
            name='KnackIdeaImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'knacks/images/', blank=True)),
                ('knack_idea', models.ForeignKey(to='knacks.KnackIdea')),
            ],
        ),
    ]
