# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0018_auto_20160201_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='description',
            name='user',
        ),
        migrations.AddField(
            model_name='knackuser',
            name='about_me',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='grand_total',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='payment_paypal',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='payment_venmo',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='public_profile_url',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knackuser',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name='knackuser',
            name='college'
        ),
        migrations.AddField(
            model_name='knackuser',
            name='college',
            field=models.ForeignKey(blank=True, to='user_auth.College', null=True),
        ),
        migrations.DeleteModel(
            name='Description',
        ),
        migrations.AddField(
            model_name='knackuser',
            name='year',
            field=models.ForeignKey(blank=True, to='user_auth.Year', null=True),
        ),
    ]
