from django.contrib import admin
import admin_thumbnails

from store.models import Product, ProductGallery, Size


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.StackedInline):

    model = ProductGallery
    extra = 1


class ProductSizeInline(admin.StackedInline):

    model = Size
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    list_display = ('article', 'brand', 'category', 'price', 'is_recommend')
    list_display_links = ('article', 'brand')
    exclude = ['slug', 'views']
    inlines = [ProductGalleryInline, ProductSizeInline]


admin.site.register(Product, ProductAdmin)
