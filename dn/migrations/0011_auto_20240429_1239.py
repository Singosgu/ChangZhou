# Generated by Django 3.1.14 on 2024-04-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dn', '0010_auto_20240416_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickingSumModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txnid', models.CharField(default='', max_length=255, verbose_name='tp Code')),
                ('order_line', models.SmallIntegerField(default=1, verbose_name='Order Line')),
                ('order_type', models.CharField(default='', max_length=255, verbose_name='Order Type')),
                ('trackingnumber', models.CharField(default='', max_length=255, verbose_name='Tracking Number')),
                ('carrier', models.CharField(default='', max_length=255, verbose_name='Carrier')),
                ('mian_dan', models.TextField(default='', verbose_name='Mian Dan')),
                ('have_mian_dan', models.BooleanField(default=False, verbose_name='Have Mian Dan')),
                ('dn_code', models.CharField(max_length=255, verbose_name='DN Code')),
                ('picker', models.CharField(default='', max_length=255, verbose_name='Picker')),
                ('picking_status', models.SmallIntegerField(default=0, verbose_name='Picking Status')),
                ('creater', models.CharField(max_length=255, verbose_name='Who Created')),
                ('bar_code', models.CharField(default='', max_length=255, verbose_name='Bar Code')),
                ('openid', models.CharField(max_length=255, verbose_name='Openid')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time')),
            ],
            options={
                'verbose_name': 'Picking Sum',
                'verbose_name_plural': 'Picking Sum',
                'db_table': 'pickingsum',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='pickinglistmodel',
            name='carrier',
            field=models.CharField(default='', max_length=255, verbose_name='Carrier'),
        ),
        migrations.AddField(
            model_name='pickinglistmodel',
            name='have_mian_dan',
            field=models.BooleanField(default=False, verbose_name='Have Mian Dan'),
        ),
        migrations.AddField(
            model_name='pickinglistmodel',
            name='mian_dan',
            field=models.TextField(default='', verbose_name='Mian Dan'),
        ),
        migrations.AddField(
            model_name='pickinglistmodel',
            name='order_line',
            field=models.SmallIntegerField(default=1, verbose_name='Order Line'),
        ),
        migrations.AddField(
            model_name='pickinglistmodel',
            name='order_type',
            field=models.CharField(default='', max_length=255, verbose_name='Order Type'),
        ),
        migrations.AddField(
            model_name='pickinglistmodel',
            name='trackingnumber',
            field=models.CharField(default='', max_length=255, verbose_name='Tracking Number'),
        ),
    ]