from django.shortcuts import render, get_object_or_404

from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    ancestor = None
    category = Category.objects.get(slug=category_slug)

    if category.is_root_node():
        categories = category.get_children()
        category_id = category.id
        products = []
        root = category.get_children()
        for child in root:
            qs = Product.objects.filter(category=child, is_available=True).order_by('-modified_date')
            for product in qs:
                products.append(product)
    else:
        category = get_object_or_404(Category, slug=category_slug)
        ancestor = category.get_ancestors(ascending=False, include_self=False).first()
        category_id = ancestor.id
        categories = ancestor.get_children()
        products = Product.objects.filter(category=category, is_available=True)

    context = {
        'products': products,
        'category': category,
        'categories': categories,
        'ancestor': ancestor,
        'category_id': category_id
    }
    return render(request, 'store/category_detail.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)
