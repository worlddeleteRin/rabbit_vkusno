# Generated by Django 3.1.3 on 2021-03-06 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20210306_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='imgname',
        ),
        migrations.RemoveField(
            model_name='product',
            name='imgname',
        ),
    ]