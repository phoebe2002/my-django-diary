# Generated by Django 5.0.1 on 2024-01-28 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mywdiary', '0006_alter_diaryentry_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diaryentry',
            name='user',
        ),
    ]
