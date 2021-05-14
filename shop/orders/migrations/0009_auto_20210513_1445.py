# Generated by Django 3.2 on 2021-05-13 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20210424_0315'),
        ('orders', '0008_auto_20210423_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='size',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='store.size', verbose_name='Размер'),
            preserve_default=False,
        ),
    ]