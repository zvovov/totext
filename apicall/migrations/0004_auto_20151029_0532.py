# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0003_auto_20151029_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='link',
            name='linkip',
            field=models.CharField(max_length=64, default=datetime.datetime(2015, 10, 29, 0, 1, 15, 925771, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='link',
            name='linktype',
            field=models.CharField(max_length=1, default=2015),
            preserve_default=False,
        ),
    ]
