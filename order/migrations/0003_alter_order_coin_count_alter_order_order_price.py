# Generated by Django 4.2 on 2023-04-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_coin_amount_order_coin_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coin_count',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_price',
            field=models.PositiveIntegerField(),
        ),
    ]
