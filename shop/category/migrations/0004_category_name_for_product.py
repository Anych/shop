# Generated by Django 3.2 on 2021-05-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_for_product',
            field=models.CharField(max_length=50, null=True, verbose_name='Наименование'),
        ),
    ]
