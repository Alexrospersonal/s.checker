# Generated by Django 4.1.2 on 2022-12-14 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0023_alter_product_options_alter_user_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dpi',
            field=models.SmallIntegerField(null=True, verbose_name='DPI'),
        ),
    ]
