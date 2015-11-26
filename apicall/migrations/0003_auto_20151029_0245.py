# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0002_auto_20151029_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='created',
        ),
        migrations.RemoveField(
            model_name='link',
            name='linkip',
        ),
        migrations.RemoveField(
            model_name='link',
            name='linktype',
        ),
    ]
