# Generated by Django 3.1.3 on 2021-03-02 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_product_ves'),
        ('cart', '0021_remove_coupon_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='products.Category'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='products.Product'),
        ),
    ]