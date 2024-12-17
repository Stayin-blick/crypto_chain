# Generated by Django 4.2.16 on 2024-12-17 19:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('bio', models.TextField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(blank=True, related_name='community_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
