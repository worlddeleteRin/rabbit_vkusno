# Generated by Django 3.1.3 on 2021-02-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bonus',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
