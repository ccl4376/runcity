# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import runner.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Runone',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(null=True, blank=True, max_length=255)),
                ('useredit', models.CharField(null=True, blank=True, max_length=32)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to=runner.models.get_imagep_Runone, blank=True)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(upload_to=runner.models.get_image_path)),
                ('runshow', models.ForeignKey(related_name='uploads', to='runner.Runone')),
            ],
        ),
    ]
