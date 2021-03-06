from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView

from category.models import Category
from orders.models import OrderProduct
from store.forms import ReviewForm, QuestionForm
from store.models import Product, ReviewRating, ProductGallery, Size, ProductFeatures, CustomerQuestion
from store.utils import question_email


class Store(ListView):

    model = Category
    template_name = 'store/category_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        ancestor = None
        if self.kwargs['category_slug']:
            category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            if category.is_root_node():
                categories = category.get_descendants(include_self=False)
                products = Product.objects.filter(category__in=categories, size__stock__gt=0).\
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
                popular_products = products.filter(views__gt=1)
                products_count = len(products)
            else:
                ancestor = category.get_ancestors(ascending=False, include_self=False).first()
                print(123)
                products = Product.objects.filter(category=category, size__stock__gt=0).\
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
                popular_products = products.filter(views__gt=1)
                products_count = len(products)
        else:
            category = Category.objects.get(id=1)
            categories = category.get_children()
            products = Product.objects.filter(category__in=categories, size__stock__gt=0). \
                order_by('-is_recommend', '-modified_date').distinct().select_related()
            products_count = products.count()
            popular_products = products.filter(views__gt=1)

        context = {
                'products': products,
                'popular_products': popular_products,
                'category': category,
                'ancestor': ancestor,
                'products_count': products_count,
            }
        return context


def store(request, category_slug=None):
    ancestor = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        if category.is_root_node():
            categories = category.get_descendants(include_self=False)
            products = Product.objects.filter(category__in=categories, size__stock__gt=0).\
                order_by('-is_recommend', '-modified_date').distinct().select_related()
            popular_products = products.filter(views__gt=1)
            products_count = len(products)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
        else:
            ancestor = category.get_ancestors(ascending=False, include_self=False).first()
            products = Product.objects.filter(category=category, size__stock__gt=0).\
                order_by('-is_recommend', '-modified_date').distinct().select_related()
            popular_products = products.filter(views__gt=1)
            products_count = products.count()
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
    else:
        category = Category.objects.get(id=1)
        categories = category.get_descendants(include_self=False)
        products = Product.objects.filter(category__in=categories, size__stock__gt=0).\
            order_by('-is_recommend', '-modified_date').distinct().select_related()
        products_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
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

    product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    product.increment_views()

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True).select_related()
    average_review = product.average_review
    count_review = product.count_review
    sizes = Size.objects.filter(product=product, stock__gt=0).select_related()

    product_gallery = ProductGallery.objects.filter(product=product).select_related()

    product_features = ProductFeatures.objects.filter(product=product).select_related()

    context = {
        'product': product,
        'order_product': order_product,
        'reviews': reviews,
        'sizes': sizes,
        'product_gallery': product_gallery,
        'average_review': average_review,
        'count_review': count_review,
        'product_features': product_features,
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
            messages.success(request, '??????????????! ?????? ?????????? ????????????????')
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
                messages.success(request, '??????????????! ?????? ?????????? ??????????????????????.')
                return redirect(url)


def ask_question(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = CustomerQuestion()
            data.email = form.cleaned_data['email']
            data.question = form.cleaned_data['question']
            data.name = form.cleaned_data['name']
            data.product_id = product_id
            if request.user.is_authenticated:
                data.user_id = request.user.id
            else:
                data.user_id = None
            data.save()
            messages.success(request, '??????????????! ?????? ???????????? ?????? ??????????????????.')
            question_email(data.name, data.email, data.question, url)
            return redirect(url)


def sales(request, sales_slug=None):
    ancestor = None

    if sales_slug is not None:
        category = get_object_or_404(Category, slug=sales_slug)
        if category.is_root_node():
            categories = category.get_descendants(include_self=False)
            products = Product.objects.filter(category__in=categories, is_discount=True, size__stock__gt=0)\
                .order_by('-is_recommend', '-modified_date').distinct().select_related()
            popular_products = products.filter(views__gt=1)
            products_count = len(products)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)

        else:
            ancestor = category.get_ancestors(ascending=False, include_self=False).first()
            categories = ancestor.get_children()
            products = Product.objects.filter(category=category, is_discount=True, size__stock__gt=0)\
                .order_by('-is_recommend', '-modified_date').distinct().select_related()
            popular_products = products.filter(views__gt=1)
            products_count = products.count()
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
    else:
        products = Product.objects.filter(is_discount=True, size__stock__gt=0).distinct().select_related()\
            .order_by('-is_recommend', '-modified_date')
        products_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        category = Category.objects.get(id=1)
        categories = category.get_children()
        popular_products = products.filter(views__gt=1)

    context = {
            'sales_slug': sales_slug,
            'products': paged_products,
            'popular_products': popular_products,
            'category': category,
            'categories': categories,
            'ancestor': ancestor,
            'products_count': products_count,
        }
    return render(request, 'store/category_detail.html', context)
