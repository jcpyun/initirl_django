# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0008_auto_20150726_0423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='join',
            old_name='invited_by',
            new_name='friend',
        ),
    ]
