from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.cart import Cart
from apps.orders.forms import CheckoutForm
from apps.orders.models import Order
from apps.orders.services import build_whatsapp_url, create_order_from_cart


def checkout(request):
    cart = Cart(request)
    if cart.is_empty:
        messages.info(request, "Tu carrito esta vacio.")
        return redirect("catalog:product_list")

    initial = {}
    if request.user.is_authenticated:
        initial = {
            "customer_name": request.user.get_full_name() or request.user.username,
            "customer_email": request.user.email,
        }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = create_order_from_cart(cart, form.cleaned_data, request.user)
            cart.clear()
            messages.success(request, f"Pedido {order.code} creado correctamente.")
            return redirect(order.get_absolute_url())
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "orders/checkout.html", {"cart": cart, "form": form})


def order_detail(request, code):
    order = get_object_or_404(Order.objects.prefetch_related("items"), code=code)
    return render(
        request,
        "orders/order_detail.html",
        {"order": order, "whatsapp_url": build_whatsapp_url(order)},
    )

# Create your views here.
