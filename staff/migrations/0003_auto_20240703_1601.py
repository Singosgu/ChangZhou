# Generated by Django 3.1.14 on 2024-07-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_listmodel_laneway'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listmodel',
            name='laneway',
        ),
        migrations.AddField(
            model_name='listmodel',
            name='bin_data',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bin Data'),
        ),
    ]
