# Generated by Django 3.2 on 2021-05-18 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_auto_20210516_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Бренд', 'verbose_name_plural': 'Бренды'},
        ),
    ]