from django.contrib import admin
import admin_thumbnails

from store.models import Product, ProductGallery, Size, ProductFeatures


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.StackedInline):

    model = ProductGallery
    extra = 1


class ProductSizeInline(admin.StackedInline):

    model = Size
    extra = 1


class ProductFeatureInline(admin.StackedInline):

    model = ProductFeatures
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    list_display = ('article', 'brand', 'category', 'price', 'is_recommend')
    list_display_links = ('article', 'brand')
    exclude = ['slug', 'views']
    inlines = [ProductFeatureInline, ProductGalleryInline, ProductSizeInline]


admin.site.register(Product, ProductAdmin)
