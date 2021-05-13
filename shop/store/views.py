from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from store.forms import ReviewForm
from store.models import Product, ReviewRating, ProductGallery, Size


def store(request, category_slug=None):
    ancestor = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        if category.is_root_node():
            categories = category.get_descendants(include_self=False)
            products = Product.objects.filter(category__in=categories)\
                .order_by('-is_recommend', '-modified_date').select_related()
            popular_products = products.filter(views__gt=1)
            products_count = len(products)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
        else:
            ancestor = category.get_ancestors(ascending=False, include_self=False).first()
            categories = ancestor.get_children()
            products = Product.objects.filter(category=category)\
                .order_by('-is_recommend', '-modified_date').select_related()
            popular_products = products.filter(views__gt=1)
            products_count = products.count()
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().order_by('-is_recommend', '-modified_date').select_related()
        products_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        category = Category.objects.get(id=1)
        categories = category.get_children()
        popular_products = products.filter(views__gt=1)

    context = {
            'products': paged_products,
            'popular_products': popular_products,
            'category': category,
            'categories': categories,
            'ancestor': ancestor,
            'products_count': products_count,
        }
    return render(request, 'store/category_detail.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        category = Category.objects.get(slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        product.increment_views()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True).select_related()
    average_review = Product.average_review(product)
    count_review = Product.count_review(product)

    sizes = Size.objects.filter(product__slug=product_slug, stock__gt=0)
    own_color = Product.own_color(product)

    product_gallery = ProductGallery.objects.filter(product__slug=product_slug)

    context = {
        'product': product,
        'category': category,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'sizes': sizes,
        'own_color': own_color,
        'product_gallery': product_gallery,
        'average_review': average_review,
        'count_review': count_review,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = Product.objects.order_by('-create_date')
    products_count = products.count()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = products.filter(name__icontains=keyword)
            products_count = products.count()

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
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
