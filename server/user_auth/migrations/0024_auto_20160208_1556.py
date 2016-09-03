# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0023_auto_20160208_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='payment_paypal',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knackuser',
            name='payment_venmo',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knackuser',
            name='public_profile_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
