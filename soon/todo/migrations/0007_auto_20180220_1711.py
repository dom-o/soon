# Generated by Django 2.0.2 on 2018-02-20 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20180220_1711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='durations',
            new_name='duration',
        ),
    ]
