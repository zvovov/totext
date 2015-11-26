# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0004_auto_20151029_0532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='linktype',
        ),
    ]
