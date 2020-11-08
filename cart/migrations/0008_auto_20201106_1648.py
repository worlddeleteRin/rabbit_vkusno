# Generated by Django 3.0.8 on 2020-11-06 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_remove_order_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Order'),
        ),
    ]