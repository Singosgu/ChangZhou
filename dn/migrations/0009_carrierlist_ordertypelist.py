# Generated by Django 3.1.14 on 2024-04-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dn', '0008_auto_20240412_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarrierList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrier', models.CharField(max_length=255, verbose_name='Order Type')),
            ],
            options={
                'verbose_name': 'Carrier List',
                'verbose_name_plural': 'Carrier List',
                'db_table': 'carrierlist',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OrderTypeList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(max_length=255, verbose_name='Order Type')),
            ],
            options={
                'verbose_name': 'Order Type List',
                'verbose_name_plural': 'Order Type List',
                'db_table': 'ordertypelist',
                'ordering': ['-id'],
            },
        ),
    ]