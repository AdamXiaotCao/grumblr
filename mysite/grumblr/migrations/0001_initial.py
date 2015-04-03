# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(default=b'', max_length=200, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('person_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(default=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grumbl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('picture', models.ImageField(upload_to=b'grumbl-photos', blank=True)),
                ('comments', models.ManyToManyField(to='grumblr.Comment', blank=True)),
                ('dislikes', models.ManyToManyField(to='grumblr.Dislike', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(default=b'', max_length=30, blank=True)),
                ('email_address', models.CharField(max_length=50)),
                ('description', models.CharField(default=b'', max_length=200, blank=True)),
                ('picture', models.ImageField(default=b'/media/user-photos/default.jpg', upload_to=b'user-photos', blank=True)),
                ('blocks', models.ManyToManyField(related_name='blocks_rel_+', to='grumblr.Person')),
                ('follows', models.ManyToManyField(related_name='follows_rel_+', to='grumblr.Person')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='grumbl',
            name='person',
            field=models.ForeignKey(to='grumblr.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='person',
            field=models.ForeignKey(to='grumblr.Person'),
            preserve_default=True,
        ),
    ]
