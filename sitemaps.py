from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product, Category


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.filter(is_active=True)


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['products:home', 'products:product_list']

    def location(self, item):
        return reverse(item)
