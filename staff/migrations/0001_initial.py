# Generated by Django 3.1.14 on 2024-07-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_name', models.CharField(max_length=255, verbose_name='Staff Name')),
                ('staff_type', models.CharField(max_length=255, verbose_name='Staff Type')),
                ('check_code', models.IntegerField(default=8888, verbose_name='Check Code')),
                ('openid', models.CharField(max_length=255, verbose_name='Openid')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Delete Label')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time')),
                ('error_check_code_counter', models.IntegerField(default=0, verbose_name='check_code error counter')),
                ('is_lock', models.BooleanField(default=False, verbose_name='Whether the lock')),
                ('picking_task', models.SmallIntegerField(default=0, verbose_name='是否有拣货任务')),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
                'db_table': 'staff',
                'ordering': ['staff_name'],
            },
        ),
        migrations.CreateModel(
            name='TypeListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_type', models.CharField(max_length=255, verbose_name='Staff Type')),
                ('openid', models.CharField(max_length=255, verbose_name='Openid')),
                ('creater', models.CharField(max_length=255, verbose_name='Creater')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time')),
            ],
            options={
                'verbose_name': 'Staff Type',
                'verbose_name_plural': 'Staff Type',
                'db_table': 'stafftype',
                'ordering': ['staff_type'],
            },
        ),
    ]
