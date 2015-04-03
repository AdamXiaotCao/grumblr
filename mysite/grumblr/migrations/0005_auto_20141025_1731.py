# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_remove_dislike_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='blocks',
            field=models.ManyToManyField(related_name=b'blocked+', to=b'grumblr.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='follows',
            field=models.ManyToManyField(related_name=b'followed+', to=b'grumblr.Person'),
        ),
    ]
