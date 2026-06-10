from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Category, SubCategory, Product, Review, NewsletterSubscriber
from .forms import ReviewForm, NewsletterForm


def home_view(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    bestsellers = Product.objects.filter(is_active=True, is_bestseller=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    newsletter_form = NewsletterForm()
    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'categories': categories,
        'newsletter_form': newsletter_form,
    })


def product_list_view(request):
    products = Product.objects.filter(is_active=True).select_related('subcategory__category')
    categories = Category.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    subcategory_slug = request.GET.get('subcategory')
    search_query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')
    in_stock = request.GET.get('in_stock')

    if category_slug:
        products = products.filter(subcategory__category__slug=category_slug)
    if subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subcategory__name__icontains=search_query) |
            Q(subcategory__category__name__icontains=search_query)
        )
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    sort_options = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'price_low': 'price',
        'price_high': '-price',
        'name': 'name',
        'rating': '-reviews__rating',
    }
    products = products.annotate(avg_rating=Avg('reviews__rating'))
    products = products.order_by(sort_options.get(sort, '-created_at')).distinct()

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    return render(request, 'products/product_list.html', {
        'products': products_page,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_slug,
        'current_subcategory': subcategory_slug,
        'current_sort': sort,
    })


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.filter(is_active=True).select_related('subcategory__category').prefetch_related('images', 'reviews__user'),
        slug=slug
    )
    related_products = Product.objects.filter(
        subcategory=product.subcategory, is_active=True
    ).exclude(id=product.id)[:4]

    review_form = None
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated and not user_review:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('products:product_detail', slug=slug)

    reviews = product.reviews.filter(is_approved=True).select_related('user')
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(subcategory__category=category, is_active=True)
    paginator = Paginator(products, 12)
    products_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'products/category.html', {
        'category': category,
        'products': products_page,
    })


def subcategory_view(request, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug, is_active=True)
    products = Product.objects.filter(subcategory=subcategory, is_active=True)
    paginator = Paginator(products, 12)
    products_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'products/subcategory.html', {
        'subcategory': subcategory,
        'products': products_page,
    })


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'Successfully subscribed to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'products:home'))
