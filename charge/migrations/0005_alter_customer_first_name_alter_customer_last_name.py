# Generated by Django 4.2.4 on 2023-08-27 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charge', '0004_customer_charge_alter_seller_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
