# Generated by Django 3.1.3 on 2021-03-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0030_auto_20210321_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='bonus_used',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]