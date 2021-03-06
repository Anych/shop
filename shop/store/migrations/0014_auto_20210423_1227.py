# Generated by Django 3.2 on 2021-04-23 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210423_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Размер скидки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_discount',
            field=models.BooleanField(default=False, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(max_length=100, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='size',
            name='stock',
            field=models.IntegerField(default=1, verbose_name='Колличество'),
        ),
    ]
