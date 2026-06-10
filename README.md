# ShopVerse - Production-Ready Django E-Commerce Platform

A complete e-commerce website built with Django, Bootstrap 5, and modern best practices.

## Features

- User authentication (register, login, logout, password reset, profile)
- Product catalog with categories, subcategories, search, filter, and sort
- Session-based cart for guests, database cart for logged-in users
- Checkout with shipping/billing addresses
- Order history, tracking, and cancellation
- Wishlist functionality
- Product reviews with star ratings
- Customized admin dashboard with statistics
- SEO-friendly URLs, meta tags, and sitemap
- Deployment ready for Render with PostgreSQL

## Quick Start (Windows)

### 1. Prerequisites
- Python 3.10+ installed
- Git (optional)

### 2. Setup

```powershell
cd d:\Django
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py populate_data
python manage.py runserver
```

### 3. Access the Site
- **Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Admin Login:** username `admin`, password `admin123`

## Deploy on Render

1. Push this project to a GitHub repository.
2. Create a new **Web Service** on [Render](https://render.com).
3. Connect your GitHub repo.
4. Render will detect `render.yaml` automatically, or configure manually:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn config.wsgi:application`
5. Add environment variables:
   - `SECRET_KEY` - generate a secure random key
   - `DEBUG` - `False`
   - `ALLOWED_HOSTS` - your-app.onrender.com
   - `DATABASE_URL` - from Render PostgreSQL database
6. Create a PostgreSQL database on Render and link it.
7. After deploy, run `python manage.py populate_data` via Render Shell.

## Project Structure

```
├── accounts/       # Authentication & user profiles
├── products/       # Products, categories, reviews
├── cart/           # Shopping cart
├── orders/         # Checkout & orders
├── wishlist/       # Wishlist
├── config/         # Project settings
├── templates/      # HTML templates
├── static/         # CSS, JS
└── media/          # Uploaded files
```

## Environment Variables

Copy `.env.example` to `.env` for local development:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For production with PostgreSQL, set `DATABASE_URL`.
