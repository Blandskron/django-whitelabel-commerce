from urllib.parse import quote

from django.db import transaction

from apps.branding.models import StoreSettings
from apps.orders.models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(cart, cleaned_data, user=None):
    order = Order.objects.create(
        user=user if user and user.is_authenticated else None,
        subtotal=cart.subtotal,
        total=cart.total,
        **cleaned_data,
    )
    for item in cart:
        product = item["product"]
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            unit_price=item["unit_price"],
            quantity=item["quantity"],
            line_total=item["line_total"],
        )
        if product.stock >= item["quantity"]:
            product.stock -= item["quantity"]
            product.save(update_fields=["stock", "updated_at"])
    return order


def build_whatsapp_url(order):
    settings = StoreSettings.load()
    number = "".join(char for char in settings.whatsapp_number if char.isdigit())
    lines = [
        f"Hola, quiero confirmar el pedido {order.code}.",
        "",
        "Detalle:",
    ]
    for item in order.items.all():
        lines.append(f"- {item.quantity} x {item.product_name}: {settings.currency} {item.line_total:,}")
    lines.extend(
        [
            "",
            f"Total: {settings.currency} {order.total:,}",
            f"Nombre: {order.customer_name}",
            f"Telefono: {order.customer_phone}",
        ]
    )
    if order.shipping_address:
        lines.append(f"Direccion: {order.shipping_address}")
    if order.customer_note:
        lines.append(f"Comentario: {order.customer_note}")
    message = quote("\n".join(lines))
    return f"https://wa.me/{number}?text={message}" if number else ""
