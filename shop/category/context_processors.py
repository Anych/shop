from category.models import Category


def menu_links(request):
    links = Category.objects.filter(level=0).order_by('id')
    return dict(links=links)
