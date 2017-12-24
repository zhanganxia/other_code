# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20171224_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indextypegoodsbanner',
            name='sku',
        ),
        migrations.RemoveField(
            model_name='indextypegoodsbanner',
            name='type',
        ),
    ]
