# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_fuzai'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='other',
            field=models.TextField(default=b'', verbose_name=''),
        ),
    ]
