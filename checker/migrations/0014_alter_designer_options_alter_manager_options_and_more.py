# Generated by Django 4.1.2 on 2022-11-23 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0013_product_designer_product_manager'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='designer',
            options={'verbose_name': 'Дизайнер', 'verbose_name_plural': 'Дизайнери'},
        ),
        migrations.AlterModelOptions(
            name='manager',
            options={'verbose_name': 'Менеджер', 'verbose_name_plural': 'Менеджери'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='back_image',
        ),
        migrations.AddField(
            model_name='product',
            name='front_smaller_image',
            field=models.ImageField(null=True, upload_to='img/smaller', verbose_name='Лице міні'),
        ),
    ]
