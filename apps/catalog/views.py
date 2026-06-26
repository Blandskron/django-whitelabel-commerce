from django.shortcuts import get_object_or_404, render

from apps.catalog.models import Category, Product


def product_list(request):
    products = Product.objects.select_related("category").filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    return render(
        request,
        "catalog/product_list.html",
        {"products": products, "categories": categories},
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images"),
        slug=slug,
        is_active=True,
    )
    return render(request, "catalog/product_detail.html", {"product": product})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    return render(
        request,
        "catalog/category_detail.html",
        {"category": category, "products": products},
    )

# Create your views here.
