# Generated by Django 3.2 on 2021-04-23 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210423_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='another_color',
            field=models.ManyToManyField(blank=True, null=True, to='store.Product', verbose_name='Другой цвет'),
        ),
    ]
