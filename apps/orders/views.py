from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.cart import Cart
from apps.orders.forms import CheckoutForm
from apps.orders.models import Order
from apps.orders.services import (
    InsufficientStockError,
    build_whatsapp_url,
    create_order_from_cart,
)

GUEST_ORDER_SESSION_KEY = "guest_order_codes"


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
            try:
                order = create_order_from_cart(cart, form.cleaned_data, request.user)
            except InsufficientStockError as error:
                messages.error(request, str(error))
                return redirect("cart:detail")
            if not request.user.is_authenticated:
                guest_orders = request.session.get(GUEST_ORDER_SESSION_KEY, [])
                request.session[GUEST_ORDER_SESSION_KEY] = [*guest_orders[-9:], order.code]
            cart.clear()
            messages.success(request, f"Pedido {order.code} creado correctamente.")
            return redirect(order.get_absolute_url())
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "orders/checkout.html", {"cart": cart, "form": form})


def order_detail(request, code):
    order = get_object_or_404(Order.objects.prefetch_related("items"), code=code)
    owns_order = request.user.is_authenticated and order.user_id == request.user.id
    has_guest_access = code in request.session.get(GUEST_ORDER_SESSION_KEY, [])
    if not (request.user.is_staff or owns_order or has_guest_access):
        # Respondemos como si no existiera para no revelar pedidos predecibles.
        raise Http404("Pedido no encontrado")
    return render(
        request,
        "orders/order_detail.html",
        {"order": order, "whatsapp_url": build_whatsapp_url(order)},
    )
