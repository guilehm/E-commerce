# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('oticas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='dono_ano',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='carrinho',
            name='dono',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
