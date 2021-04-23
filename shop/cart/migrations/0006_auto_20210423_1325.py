# Generated by Django 3.2 on 2021-04-23 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20210423_1234'),
        ('cart', '0005_cartitem_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='color',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.ManyToManyField(blank=True, to='store.Size'),
        ),
    ]