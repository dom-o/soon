# Generated by Django 2.0.2 on 2018-02-12 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('descr', models.TextField(max_length=500)),
                ('priority', models.IntegerField(default=-1, unique=True)),
            ],
        ),
    ]
