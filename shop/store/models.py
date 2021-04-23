from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from mptt.fields import TreeForeignKey

from accounts.models import Account
from category.models import Category, Brand
from store.utils import gen_slug


class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=200, verbose_name='Название')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Бренд')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    image1 = models.ImageField(upload_to='photos/products')
    image2 = models.ImageField(upload_to='photos/products')
    is_discount = models.BooleanField(default=True, verbose_name='Скидка?')
    discount_amount = models.IntegerField(verbose_name='Размер скидки')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.name, self.category)
        super().save(*args, **kwargs)


class VariationManager(models.Manager):

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


VARIATION_CATEGORY_CHOICE = (
    ('цвет', 'Цвет'),
    ('размер', 'Размер'),
)


class Color(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICE)
    variation_value = models.CharField(max_length=100)
    stock = models.IntegerField(verbose_name='В наличии')
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


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
        return self.product.name


class ProductGallery(models.Model):

    product = models.ForeignKey(Color, default=None, on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, upload_to='store/products')

    def __str__(self):
        return self.product.name
