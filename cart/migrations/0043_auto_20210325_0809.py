# Generated by Django 3.1.3 on 2021-03-25 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0042_cart_delivery_discount_use'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='delivery_method',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cart',
            name='payment_method',
            field=models.IntegerField(default=1),
        ),
    ]
