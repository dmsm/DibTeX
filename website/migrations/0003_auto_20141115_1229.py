# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20141115_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='points',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
