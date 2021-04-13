from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey

from category.models import Category


class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True, verbose_name='В наличии?')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})


class VariationManager(models.Manager):

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


VARIATION_CATEGORY_CHOICE = (
    ('color', 'Цвет'),
    ('size', 'Размер'),
)


class Variation(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICE)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
