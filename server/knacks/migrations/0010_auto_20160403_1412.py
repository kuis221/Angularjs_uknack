# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knacks', '0009_auto_20160329_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knackidea',
            old_name='rate',
            new_name='price',
        ),
        migrations.AlterField(
            model_name='knack',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='knack',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='knackidea',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='knackidea',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
