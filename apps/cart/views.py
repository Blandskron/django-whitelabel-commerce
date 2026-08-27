from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.branding.models import StoreSettings
from apps.cart.cart import Cart
from apps.catalog.models import Product


def _quantity_from_request(request):
    """Return a positive quantity or ``None`` for malformed user input."""
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        return None
    return quantity if quantity > 0 else None


def _stock_allows(product, quantity):
    store_settings = StoreSettings.load()
    return store_settings.allow_out_of_stock_orders or quantity <= product.stock


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = _quantity_from_request(request)
    if quantity is None:
        messages.error(request, "Ingresa una cantidad valida mayor que cero.")
        return redirect(product.get_absolute_url())

    cart = Cart(request)
    requested_total = cart.data.get(str(product.id), 0) + quantity
    if not _stock_allows(product, requested_total):
        messages.error(request, f"Solo hay {product.stock} unidades disponibles.")
        return redirect(product.get_absolute_url())

    cart.add(product, quantity=quantity)
    messages.success(request, f"{product.name} fue agregado al carrito.")
    next_url = request.POST.get("next")
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = product.get_absolute_url()
    return redirect(next_url)


@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = _quantity_from_request(request)
    if quantity is None:
        messages.error(request, "Ingresa una cantidad valida mayor que cero.")
        return redirect("cart:detail")
    if not _stock_allows(product, quantity):
        messages.error(request, f"Solo hay {product.stock} unidades disponibles.")
        return redirect("cart:detail")
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
