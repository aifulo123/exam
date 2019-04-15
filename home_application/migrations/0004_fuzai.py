# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_host_biz_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuZai',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True)),
                ('ip', models.CharField(max_length=128, verbose_name='')),
                ('value', models.CharField(max_length=128, verbose_name='')),
            ],
        ),
    ]
