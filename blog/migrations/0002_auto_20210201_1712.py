# Generated by Django 3.1.5 on 2021-02-01 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='titlte',
            new_name='title',
        ),
    ]
