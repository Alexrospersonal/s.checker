# Generated by Django 4.1.2 on 2022-11-22 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0010_remove_user_position_alter_product_manager_designer_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Position',
        ),
    ]
