# Generated by Django 2.1.4 on 2021-09-04 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goblins', '0002_auto_20210903_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='logged',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
