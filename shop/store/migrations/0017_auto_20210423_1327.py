# Generated by Django 3.2 on 2021-04-23 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210423_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='another_color',
        ),
        migrations.AddField(
            model_name='product',
            name='another_color',
            field=models.ManyToManyField(blank=True, null=True, related_name='_store_product_another_color_+', to='store.Product', verbose_name='Другой цвет'),
        ),
    ]
