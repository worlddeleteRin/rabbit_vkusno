# Generated by Django 3.1.3 on 2021-03-01 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_auto_20210223_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('in_progress', 'В процессе'), ('completed', 'Завершен'), ('cancelled', 'Отменен')], default='in_progress', max_length=100),
        ),
    ]
