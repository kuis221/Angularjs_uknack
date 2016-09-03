# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0028_auto_20160218_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knackuser',
            name='payment_paypal',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='knackuser',
            name='payment_venmo',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
