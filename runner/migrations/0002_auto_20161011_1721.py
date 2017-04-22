# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upload',
            old_name='runshow',
            new_name='thing',
        ),
    ]
