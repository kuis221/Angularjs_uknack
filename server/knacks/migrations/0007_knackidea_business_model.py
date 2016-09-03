# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0006_auto_20160126_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='knackidea',
            name='business_model',
            field=redactor.fields.RedactorField(default=b'', verbose_name='Business Model'),
        ),
    ]
