# Generated by Django 4.2 on 2023-04-24 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='coin_amount',
            new_name='coin_count',
        ),
    ]
