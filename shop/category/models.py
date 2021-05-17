from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование для категории')
    name_for_product = models.CharField(max_length=50, null=True, verbose_name='Наименование для продукта')
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def get_sales_url(self):
        return reverse('sales', kwargs={'sales_slug': self.slug})


class Brand(models.Model):

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'brand_slug': self.slug})
