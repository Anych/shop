# Generated by Django 3.2 on 2021-04-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20210423_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img1',
            field=models.ImageField(default=1, upload_to='store/products/%y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='img2',
            field=models.ImageField(default=1, upload_to='store/products/%y/%m/%d'),
            preserve_default=False,
        ),
    ]
