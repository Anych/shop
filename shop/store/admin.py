from django.contrib import admin
import admin_thumbnails
from django.utils.html import format_html

from store.models import Product, ReviewRating, ProductGallery, Size


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.StackedInline):

    model = ProductGallery
    extra = 1


class ProductSizeInline(admin.StackedInline):

    model = Size
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    # def thumbnail(self, object):
    #     return format_html('<img src="{}" width="40" />'.format(object.image1.url))
    # thumbnail.short_description = 'Фото продукта'

    list_display = ('name', 'price', 'category', 'is_discount')
    exclude = ['slug', 'views']
    inlines = [ProductGalleryInline, ProductSizeInline]


class SizeAdmin(admin.ModelAdmin):

    list_display = ('product',)
    list_filter = ('product',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
