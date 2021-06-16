# Generated by Django 3.2.2 on 2021-06-16 03:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='_network_user_following_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked',
            field=models.ManyToManyField(blank=True, null=True, related_name='likers', to='network.Posts'),
        ),
    ]