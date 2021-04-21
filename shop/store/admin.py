from django.contrib import admin
import admin_thumbnails

from store.models import Product, Variation, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('images')
class ProductGalleryInline(admin.TabularInline):

    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'stock', 'category', 'modified_date')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):

    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
