# Generated by Django 4.1.2 on 2022-12-05 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0020_alter_designer_designer_alter_manager_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='checker.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='checker.item', verbose_name='Елемент'),
        ),
    ]
