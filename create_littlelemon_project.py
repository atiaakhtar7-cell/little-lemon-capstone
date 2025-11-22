import os

# Base project folder
base_dir = "littlelemon"
os.makedirs(base_dir, exist_ok=True)

# Project subfolders
folders = [
    f"{base_dir}/littlelemon",
    f"{base_dir}/menu",
    f"{base_dir}/menu/templates/menu",
    f"{base_dir}/templates",
    f"{base_dir}/static/css",
    f"{base_dir}/static/img",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Dictionary of files and their content
files = {
    f"{base_dir}/manage.py": """#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'littlelemon.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
""",
    f"{base_dir}/littlelemon/__init__.py": "",
    f"{base_dir}/littlelemon/settings.py": """from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-your-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'littlelemon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'littlelemon.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""",
    f"{base_dir}/littlelemon/urls.py": """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""",
    f"{base_dir}/littlelemon/asgi.py": """import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'littlelemon.settings')
application = get_asgi_application()
""",
    f"{base_dir}/littlelemon/wsgi.py": """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'littlelemon.settings')
application = get_wsgi_application()
""",
    f"{base_dir}/menu/__init__.py": "",
    f"{base_dir}/menu/admin.py": """from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
""",
    f"{base_dir}/menu/apps.py": """from django.apps import AppConfig

class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'
""",
    f"{base_dir}/menu/models.py": """from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
""",
    f"{base_dir}/menu/views.py": """from django.shortcuts import render, get_object_or_404
from .models import MenuItem

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')

def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'menu/menu.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})
""",
    f"{base_dir}/menu/urls.py": """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('menu/<int:pk>/', views.item_detail, name='item_detail'),
]
""",
    f"{base_dir}/templates/base.html": """<!DOCTYPE html>
<html>
<head>
    <title>Little Lemon</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <header>
        <nav>
            <a href="{% url 'home' %}">Home</a>
            <a href="{% url 'about' %}">About</a>
            <a href="{% url 'menu' %}">Menu</a>
            <a href="{% url 'book' %}">Book</a>
        </nav>
    </header>

    {% block content %}{% endblock %}

    <footer>
        <p>© 2025 Little Lemon</p>
    </footer>
</body>
</html>
""",
    f"{base_dir}/templates/home.html": "{% extends 'base.html' %}\n{% block content %}\n<h1>Welcome to Little Lemon!</h1>\n{% endblock %}",
    f"{base_dir}/templates/about.html": "{% extends 'base.html' %}\n{% block content %}\n<h1>About Little Lemon</h1>\n<p>Our restaurant serves the best Mediterranean food!</p>\n{% endblock %}",
    f"{base_dir}/templates/book.html": "{% extends 'base.html' %}\n{% block content %}\n<h1>Book a Table</h1>\n<p>Reservation page coming soon!</p>\n{% endblock %}",
    f"{base_dir}/menu/templates/menu/menu.html": """{% extends 'base.html' %}
{% block content %}
<h1>Menu</h1>
<ul>
    {% for item in items %}
        <li>
            <a href="{% url 'item_detail' item.pk %}">{{ item.name }}</a> - ${{ item.price }}
        </li>
    {% empty %}
        <li>No menu items found.</li>
    {% endfor %}
</ul>
{% endblock %}""",
    f"{base_dir}/menu/templates/menu/item_detail.html": """{% extends 'base.html' %}
{% block content %}
<h1>{{ item.name }}</h1>
<p>Price: ${{ item.price }}</p>
<p>Description: {{ item.description }}</p>
{% if item.image %}
<img src="{{ item.image.url }}" alt="{{ item.name }}">
{% endif %}
{% endblock %}""",
    f"{base_dir}/static/css/style.css": """body { font-family: Arial, sans-serif; }
nav a { margin-right: 15px; text-decoration: none; }
footer { margin-top: 50px; text-align: center; }""",
    f"{base_dir}/static/img/placeholder.jpg": "",
}

# Write files
for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Project structure for 'littlelemon' created successfully!")
print("Next steps: run 'python manage.py makemigrations', 'migrate', 'createsuperuser', 'runserver'")
