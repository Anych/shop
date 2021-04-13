from django.contrib import admin

from store.models import Product, Variation


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'stock', 'category', 'modified_date')
    prepopulated_fields = {'slug': ('name',)}


class VariationAdmin(admin.ModelAdmin):

    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
