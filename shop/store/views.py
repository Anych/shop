from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from store.forms import ReviewForm
from store.models import Product, ReviewRating, ProductGallery


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

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True, )

    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    context = {
        'product': product,
        'category': category,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Спасибо! Ваш отзыв обновлён')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Спасибо! Ваш отзыв опубликован.')
                return redirect(url)
