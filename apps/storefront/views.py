from django.shortcuts import render

from apps.catalog.models import Category, Product


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related("category")[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    return render(
        request,
        "storefront/home.html",
        {"featured_products": featured_products, "categories": categories},
    )


def contact(request):
    return render(request, "storefront/contact.html")

# Create your views here.
