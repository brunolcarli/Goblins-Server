# Generated by Django 2.1.4 on 2021-09-03 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goblins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='reference',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
