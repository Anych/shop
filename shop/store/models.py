from datetime import datetime, timezone

from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from mptt.fields import TreeForeignKey

from smartfields import fields

from accounts.models import Account
from category.models import Category, Brand
from store.utils import gen_slug


class Product(models.Model):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['category', 'price', '-create_date']

    article = models.CharField(max_length=200, null=True, verbose_name='Артикул')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Бренд')
    name_of_model = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название модели')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', blank=True)
    structure = models.CharField(max_length=200, blank=True, null=True, verbose_name='Состав')
    color = models.CharField(max_length=100, verbose_name='Цвет')
    another_color = models.ManyToManyField('self', blank=True, verbose_name='Другой цвет')
    made_in = models.CharField(max_length=100, null=True, verbose_name='Производство')
    description = models.TextField(blank=True, verbose_name='Описание')
    img1 = fields.ImageField(upload_to='store/products', verbose_name='Изображение 1')
    img2 = fields.ImageField(upload_to='store/products', verbose_name='Изображение 2')
    price = models.IntegerField(verbose_name='Цена')
    is_discount = models.BooleanField(default=False, verbose_name='Скидка')
    discount_amount = models.IntegerField(blank=True, null=True, verbose_name='Размер скидки')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_recommend = models.BooleanField(default=False, verbose_name='Рекомендации')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.article} - {self.category.name_for_product}: {self.brand}'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def get_new_product(self):
        new = datetime.now(timezone.utc) - self.create_date
        if new.days <= 30:
            return new

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def discount_price(self):
        if self.is_discount:
            self.discount_price = int((int(self.price) * (100 - int(self.discount_amount))) / 100)
            return self.discount_price

    def you_save(self):
        return self.price - self.discount_price

    def stock(self):
        stocks = Size.objects.filter(product=self).aggregate(count=Count('id'))
        count = 0
        if stocks['count'] is not None:
            count = int(stocks['count'])
        return count

    def increment_views(self):
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.category.name, self.brand.name)
        super().save(*args, **kwargs)


class ProductGallery(models.Model):

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'

    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, verbose_name='Продукт')
    image = fields.ImageField(upload_to='store/products', verbose_name='Изображение')


class ProductFeatures(models.Model):

    class Meta:
        verbose_name = 'Дополниетелыное поле продукта'
        verbose_name_plural = 'Дополниетелыные поля продукта'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    value = models.CharField(max_length=200, verbose_name='Ключ')
    feature = models.CharField(max_length=200, verbose_name='Значение')


class Size(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    size = models.CharField(max_length=100, verbose_name='Размер')
    stock = models.IntegerField(default=1, verbose_name='Колличество')

    def __str__(self):
        return self.size


class ReviewRating(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    review = models.TextField(max_length=1500, blank=True, verbose_name='Отзыв')
    rating = models.FloatField(verbose_name='Рейтинг')
    ip = models.CharField(max_length=20, blank=True, verbose_name='IP')
    status = models.BooleanField(default=True, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.review


class CustomerQuestion(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    question = models.TextField(max_length=1500, blank=True, verbose_name='Вопрос')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    email = models.CharField(max_length=200, blank=True, verbose_name='Почта')
    name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.email
