# Generated by Django 3.1.3 on 2021-03-01 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_order_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_status',
            new_name='status',
        ),
    ]
