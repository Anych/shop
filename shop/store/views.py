from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    ancestor = None
    categories = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        if category.is_root_node():
            categories = category.get_children()
            category_id = category.id
            products = []
            root = category.get_children()
            for child in root:
                qs = Product.objects.filter(category=child, is_available=True)\
                    .select_related().order_by('-modified_date')
                for product in qs:
                    products.append(product)
            products_count = len(products)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
        else:
            ancestor = category.get_ancestors(ascending=False, include_self=False).first()
            category_id = ancestor.id
            categories = ancestor.get_children()
            products = Product.objects.filter(category=category, is_available=True).order_by('-modified_date')
            products_count = products.count()
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-modified_date')
        products_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        category = Category.objects.get(id=1)
        category_id = 1
        categories = category.get_children()

    context = {
            'products': paged_products,
            'category': category,
            'categories': categories,
            'ancestor': ancestor,
            'category_id': category_id,
            'products_count': products_count,
        }
    return render(request, 'store/category_detail.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        category = Category.objects.get(slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    context = {
        'product': product,
        'category': category,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-create_date').filter(name__icontains=keyword)
            products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/category_detail.html', context)
