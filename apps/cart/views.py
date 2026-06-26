from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.cart.cart import Cart
from apps.catalog.models import Product


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    Cart(request).add(product, quantity=max(quantity, 1))
    messages.success(request, f"{product.name} fue agregado al carrito.")
    return redirect(request.POST.get("next") or product.get_absolute_url())


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    Cart(request).add(product, quantity=quantity, replace=True)
    messages.success(request, "Carrito actualizado.")
    return redirect("cart:detail")


@require_POST
def remove_from_cart(request, product_id):
    Cart(request).remove(product_id)
    messages.success(request, "Producto removido del carrito.")
    return redirect("cart:detail")


@require_POST
def clear_cart(request):
    Cart(request).clear()
    messages.success(request, "Carrito vaciado.")
    return redirect("cart:detail")

# Create your views here.
