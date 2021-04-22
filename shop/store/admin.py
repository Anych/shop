from django.contrib import admin
import admin_thumbnails
from django.utils.html import format_html

from store.models import Product, Variation, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('images')
class ProductGalleryInline(admin.TabularInline):

    model = ProductGallery
    extra = 1


class VariationAdminInline(admin.StackedInline):

    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.images.url))
    thumbnail.short_description = 'Фото продукта'

    list_display = ('thumbnail', 'name', 'price', 'stock', 'category', 'modified_date')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductGalleryInline, VariationAdminInline]


class VariationAdmin(admin.ModelAdmin):

    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
