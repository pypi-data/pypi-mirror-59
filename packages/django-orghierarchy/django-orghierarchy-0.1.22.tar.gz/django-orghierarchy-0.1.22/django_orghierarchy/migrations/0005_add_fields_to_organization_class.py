# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_orghierarchy', '0004_add_affiliated_org_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationclass',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The time at which the resource was created'),
        ),
        migrations.AddField(
            model_name='organizationclass',
            name='data_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.DJANGO_ORGHIERARCHY_DATASOURCE_MODEL),
        ),
        migrations.AddField(
            model_name='organizationclass',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, help_text='The time at which the resource was updated'),
        ),
        migrations.AddField(
            model_name='organizationclass',
            name='origin_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The time at which the resource was created'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='origin_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organizationclass',
            name='id',
            field=models.CharField(editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='organizationclass',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='organizationclass',
            unique_together=set([('data_source', 'origin_id')]),
        ),
    ]
