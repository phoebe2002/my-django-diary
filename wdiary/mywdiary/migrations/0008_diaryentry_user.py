# Generated by Django 5.0.1 on 2024-01-28 01:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywdiary', '0007_remove_diaryentry_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaryentry',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
