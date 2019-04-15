# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_host_yun_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='biz_id',
            field=models.CharField(default=b'', max_length=128, verbose_name=''),
        ),
    ]
