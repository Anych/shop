# Generated by Django 3.2 on 2021-04-17 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210417_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='subject',
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='review',
            field=models.TextField(blank=True, max_length=1500, verbose_name='Отзыв'),
        ),
    ]
