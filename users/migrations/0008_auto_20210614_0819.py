# Generated by Django 3.1.5 on 2021-06-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210201_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile.png', upload_to='profile_pics'),
        ),
    ]
