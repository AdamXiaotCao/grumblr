# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0003_auto_20141024_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dislike',
            name='person',
        ),
    ]
