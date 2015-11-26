# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('linkip', models.CharField(max_length=64)),
                ('linktext', models.CharField(max_length=500)),
                ('linktype', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('userip', models.CharField(max_length=64)),
                ('visited', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
