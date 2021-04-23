from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from category.models import Category, Brand


class CategoryAdmin(DraggableMPTTAdmin):

    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
