# Generated by Django 3.1.3 on 2021-03-02 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0019_coupon_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
