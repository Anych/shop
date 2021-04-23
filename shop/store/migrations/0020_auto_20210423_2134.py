# Generated by Django 3.2 on 2021-04-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_product_another_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_recommend',
            field=models.BooleanField(default=False, verbose_name='Рекомендации'),
        ),
        migrations.AlterField(
            model_name='product',
            name='another_color',
            field=models.ManyToManyField(blank=True, related_name='_store_product_another_color_+', to='store.Product', verbose_name='Другой цвет'),
        ),
    ]
