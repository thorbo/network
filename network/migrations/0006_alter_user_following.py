# Generated by Django 3.2.2 on 2021-06-15 22:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
