from django.contrib import admin
import admin_thumbnails
from django.utils.html import format_html

from store.models import Product, Variation, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.StackedInline):

    model = ProductGallery
    extra = 1


class VariationAdminInline(admin.StackedInline):

    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image1.url))
    thumbnail.short_description = 'Фото продукта'

    list_display = ('thumbnail', 'name', 'price', 'category', 'is_discount')
    inlines = [VariationAdminInline]
    exclude = ['slug']


class VariationAdmin(admin.ModelAdmin):

    list_display = ('product', 'variation_category', 'variation_value')
    list_filter = ('product', 'variation_category', 'variation_value')
    inlines = [ProductGalleryInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
