# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True)),
                ('ip', models.CharField(max_length=128, verbose_name='')),
                ('name', models.CharField(max_length=128, verbose_name='')),
                ('system', models.CharField(max_length=128, verbose_name='')),
                ('yun', models.CharField(max_length=128, verbose_name='')),
                ('biz', models.CharField(max_length=128, verbose_name='')),
            ],
        ),
    ]
