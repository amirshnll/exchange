# Generated by Django 4.2 on 2023-04-24 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coin', '0003_remove_cointypes_minimum_purchase'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_amount', models.IntegerField()),
                ('order_price', models.IntegerField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('DONE', 'Done')], max_length=10)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coin.cointypes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
