from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, SubCategory, Product


SAMPLE_DATA = [
    {
        'category': {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest gadgets and tech'},
        'subcategories': [
            {
                'name': 'Smartphones', 'slug': 'smartphones',
                'products': [
                    {'name': 'ProPhone X15', 'slug': 'prophone-x15', 'description': 'Flagship smartphone with advanced camera and 5G connectivity.', 'price': 999.99, 'discount_price': 899.99, 'stock': 50, 'is_featured': True, 'is_bestseller': True},
                    {'name': 'BudgetPhone Lite', 'slug': 'budgetphone-lite', 'description': 'Affordable smartphone with great battery life.', 'price': 249.99, 'stock': 100, 'is_bestseller': True},
                ]
            },
            {
                'name': 'Laptops', 'slug': 'laptops',
                'products': [
                    {'name': 'UltraBook Pro 14', 'slug': 'ultrabook-pro-14', 'description': 'Lightweight laptop with powerful performance for professionals.', 'price': 1299.99, 'discount_price': 1149.99, 'stock': 30, 'is_featured': True},
                    {'name': 'GameStation Laptop', 'slug': 'gamestation-laptop', 'description': 'High-performance gaming laptop with RTX graphics.', 'price': 1599.99, 'stock': 20, 'is_bestseller': True},
                ]
            },
        ]
    },
    {
        'category': {'name': 'Fashion', 'slug': 'fashion', 'description': 'Trendy clothing and accessories'},
        'subcategories': [
            {
                'name': 'Men', 'slug': 'men',
                'products': [
                    {'name': 'Classic Denim Jacket', 'slug': 'classic-denim-jacket', 'description': 'Premium denim jacket with modern fit.', 'price': 89.99, 'discount_price': 69.99, 'stock': 75, 'is_featured': True},
                    {'name': 'Cotton Polo Shirt', 'slug': 'cotton-polo-shirt', 'description': 'Comfortable cotton polo for everyday wear.', 'price': 39.99, 'stock': 120, 'is_bestseller': True},
                ]
            },
            {
                'name': 'Women', 'slug': 'women',
                'products': [
                    {'name': 'Floral Summer Dress', 'slug': 'floral-summer-dress', 'description': 'Elegant floral dress perfect for summer occasions.', 'price': 79.99, 'discount_price': 59.99, 'stock': 60, 'is_featured': True, 'is_bestseller': True},
                    {'name': 'Leather Handbag', 'slug': 'leather-handbag', 'description': 'Genuine leather handbag with multiple compartments.', 'price': 149.99, 'stock': 40},
                ]
            },
        ]
    },
    {
        'category': {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Everything for your home'},
        'subcategories': [
            {
                'name': 'Furniture', 'slug': 'furniture',
                'products': [
                    {'name': 'Modern Office Chair', 'slug': 'modern-office-chair', 'description': 'Ergonomic office chair with lumbar support.', 'price': 299.99, 'discount_price': 249.99, 'stock': 25, 'is_featured': True},
                    {'name': 'Minimalist Desk Lamp', 'slug': 'minimalist-desk-lamp', 'description': 'Adjustable LED desk lamp with warm light.', 'price': 49.99, 'stock': 80, 'is_bestseller': True},
                ]
            },
        ]
    },
]


class Command(BaseCommand):
    help = 'Populate the database with sample e-commerce data'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@shopverse.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))

        for cat_data in SAMPLE_DATA:
            category, _ = Category.objects.get_or_create(
                slug=cat_data['category']['slug'],
                defaults=cat_data['category'],
            )
            for sub_data in cat_data['subcategories']:
                subcategory, _ = SubCategory.objects.get_or_create(
                    category=category,
                    slug=sub_data['slug'],
                    defaults={'name': sub_data['name']},
                )
                for prod_data in sub_data['products']:
                    Product.objects.get_or_create(
                        slug=prod_data['slug'],
                        defaults={**prod_data, 'subcategory': subcategory},
                    )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
