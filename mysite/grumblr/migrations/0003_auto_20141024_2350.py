# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_dislike_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dislike',
            name='person',
            field=models.ForeignKey(blank=True, to='grumblr.Person', null=True),
        ),
    ]
