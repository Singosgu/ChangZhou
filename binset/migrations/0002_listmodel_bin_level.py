# Generated by Django 3.1.14 on 2024-04-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binset', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listmodel',
            name='bin_level',
            field=models.BigIntegerField(default=1, verbose_name='Bin Level'),
        ),
    ]
