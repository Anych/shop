# Generated by Django 3.2 on 2021-04-14 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_alter_variation_variation_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, verbose_name='Номер заказа')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=15, verbose_name='Номер')),
                ('email', models.EmailField(max_length=50, verbose_name='Почта')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('order_note', models.CharField(blank=True, max_length=100, verbose_name='Примечания')),
                ('order_total', models.FloatField(verbose_name='Общая сумма')),
                ('delivery', models.FloatField(verbose_name='Стоимость доставки')),
                ('status', models.CharField(choices=[('New', 'Новый'), ('Accepted', 'Подтверждён'), ('Completed', 'Завершён'), ('Cancelled', 'Отменён')], default='New', max_length=10, verbose_name='Статус')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='В заказе')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, verbose_name='Номер оплаты')),
                ('payment_method', models.CharField(max_length=100, verbose_name='Метод оплаты')),
                ('amount_paid', models.CharField(max_length=100, verbose_name='Сумма оплаты')),
                ('status', models.CharField(max_length=100, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Колличество')),
                ('product_price', models.FloatField(verbose_name='Цена продукта')),
                ('ordered', models.BooleanField(default=False, verbose_name='Заказан')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='Оплата')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('variations', models.ManyToManyField(blank=True, to='store.Variation', verbose_name='Вариация')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='Платёж'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
