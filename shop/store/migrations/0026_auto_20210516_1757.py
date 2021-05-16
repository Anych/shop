# Generated by Django 3.2 on 2021-05-16 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_auto_20210516_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productfeatures',
            options={'verbose_name': 'Дополниетелыное поле продукта', 'verbose_name_plural': 'Дополниетелыные поля продукта'},
        ),
        migrations.AddField(
            model_name='product',
            name='made_in',
            field=models.CharField(max_length=100, null=True, verbose_name='Производство'),
        ),
        migrations.AlterField(
            model_name='productfeatures',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт'),
            preserve_default=False,
        ),
    ]
