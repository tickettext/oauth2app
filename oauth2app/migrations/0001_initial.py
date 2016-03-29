# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oauth2app.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=255, db_index=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(default=oauth2app.models.KeyGenerator(50), unique=True, max_length=50, db_index=True)),
                ('refresh_token', models.CharField(null=True, default=oauth2app.models.KeyGenerator(50), max_length=50, blank=True, unique=True, db_index=True)),
                ('mac_key', models.CharField(default=None, max_length=50, unique=True, null=True, blank=True)),
                ('issue', models.PositiveIntegerField(default=oauth2app.models.TimestampGenerator(), editable=False)),
                ('expire', models.PositiveIntegerField(default=oauth2app.models.TimestampGenerator(3600))),
                ('refreshable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
                ('key', models.CharField(default=oauth2app.models.KeyGenerator(30), unique=True, max_length=30, db_index=True)),
                ('secret', models.CharField(default=oauth2app.models.KeyGenerator(30), unique=True, max_length=30)),
                ('redirect_uri', models.URLField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=oauth2app.models.KeyGenerator(30), unique=True, max_length=30, db_index=True)),
                ('issue', models.PositiveIntegerField(default=oauth2app.models.TimestampGenerator(), editable=False)),
                ('expire', models.PositiveIntegerField(default=oauth2app.models.TimestampGenerator(120))),
                ('redirect_uri', models.URLField(null=True)),
                ('client', models.ForeignKey(to='oauth2app.Client')),
                ('scope', models.ManyToManyField(to='oauth2app.AccessRange')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MACNonce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nonce', models.CharField(max_length=30, db_index=True)),
                ('access_token', models.ForeignKey(to='oauth2app.AccessToken')),
            ],
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='client',
            field=models.ForeignKey(to='oauth2app.Client'),
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='scope',
            field=models.ManyToManyField(to='oauth2app.AccessRange'),
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
