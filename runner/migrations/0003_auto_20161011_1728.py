# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0002_auto_20161011_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upload',
            old_name='thing',
            new_name='runshow',
        ),
    ]
