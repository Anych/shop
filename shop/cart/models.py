from django.db import models

from store.models import Product, Variation


class Cart(models.Model):

    cart_id = models.CharField(max_length=255, blank=True, verbose_name='Номер корзины')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):

    class Meta:
        ordering = ['id']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    quantity = models.IntegerField(verbose_name='Колличество')
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
