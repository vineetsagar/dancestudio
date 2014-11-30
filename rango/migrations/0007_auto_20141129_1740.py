# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_auto_20141129_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventtype',
            old_name='name',
            new_name='event_type_name',
        ),
    ]
