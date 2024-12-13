# Generated by Django 4.2.16 on 2024-12-11 19:03

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='default_pfp.jpg', max_length=255, verbose_name='image'),
        ),
    ]
