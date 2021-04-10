from django.contrib import admin

from store.models import Product


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'stock', 'category', 'modified_date')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
