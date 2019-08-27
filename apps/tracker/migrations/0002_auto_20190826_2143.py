# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-27 02:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=255)),
                ('rating', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('auther', models.CharField(max_length=255)),
                ('review_date', models.CharField(max_length=255)),
                ('likes', models.CharField(max_length=5)),
                ('dislikes', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to='login.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='news',
            name='users',
        ),
        migrations.DeleteModel(
            name='News',
        ),
    ]