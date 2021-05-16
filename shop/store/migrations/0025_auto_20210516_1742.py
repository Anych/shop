# Generated by Django 3.2 on 2021-05-16 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20210516_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name': 'Галерея', 'verbose_name_plural': 'Галереи'},
        ),
        migrations.AlterField(
            model_name='product',
            name='img1',
            field=models.ImageField(upload_to='store/products', verbose_name='Изображение 1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img2',
            field=models.ImageField(upload_to='store/products', verbose_name='Изображение 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Просмотры'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=models.ImageField(upload_to='store/products', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='size',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт'),
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, verbose_name='Ключ')),
                ('feature', models.CharField(max_length=200, verbose_name='Значение')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галереи',
            },
        ),
    ]
