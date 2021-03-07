# Generated by Django 3.1.3 on 2021-02-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210227_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bonus',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
