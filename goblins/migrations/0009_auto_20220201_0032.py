# Generated by Django 2.1.4 on 2022-02-01 00:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goblins', '0008_character_goblin_class'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='character',
            unique_together={('name', 'user')},
        ),
    ]
