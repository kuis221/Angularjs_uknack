# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('receipt', models.ForeignKey(related_name='receipts', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='senders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
