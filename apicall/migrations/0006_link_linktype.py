# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0005_remove_link_linktype'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='linktype',
            field=models.CharField(max_length=1, default='i'),
            preserve_default=False,
        ),
    ]
