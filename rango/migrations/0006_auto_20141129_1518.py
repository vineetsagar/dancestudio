# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_auto_20141129_1512'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventsInstrcutors',
            new_name='EventsInstructors',
        ),
    ]
