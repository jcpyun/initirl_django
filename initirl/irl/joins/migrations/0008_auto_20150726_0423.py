# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0007_join_friend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='join',
            old_name='friend',
            new_name='invited_by',
        ),
    ]
