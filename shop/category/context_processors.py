from category.models import Category


def menu_links(request):
    links = Category.objects.select_related().filter(level=0).order_by('id')
    cloth_categories = Category.objects.get(id=1).get_descendants(include_self=False)
    shoe_categories = Category.objects.get(id=2).get_descendants(include_self=False)
    accessories_categories = Category.objects.get(id=3).get_descendants(include_self=False)
    return dict(links=links, cloth_categories=cloth_categories, shoe_categories=shoe_categories,
                accessories_categories=accessories_categories)
