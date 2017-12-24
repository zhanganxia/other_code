# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20171224_2142'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IndexTypeGoodsBanner',
        ),
    ]
