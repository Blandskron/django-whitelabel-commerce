from urllib.parse import quote

from django.db import transaction

from apps.branding.models import StoreSettings
from apps.catalog.models import Product
from apps.orders.models import Order, OrderItem


class InsufficientStockError(Exception):
    """Raised when a checkout cannot reserve the requested stock."""


@transaction.atomic
def create_order_from_cart(cart, cleaned_data, user=None):
    cart_items = list(cart)
    store_settings = StoreSettings.load()
    product_ids = [item["product"].pk for item in cart_items]
    locked_products = {
        product.pk: product
        for product in Product.objects.select_for_update().filter(pk__in=product_ids)
    }

    for item in cart_items:
        product = locked_products[item["product"].pk]
        if (
            not store_settings.allow_out_of_stock_orders
            and item["quantity"] > product.stock
        ):
            raise InsufficientStockError(
                f"{product.name} tiene {product.stock} unidades disponibles."
            )

    subtotal = sum(
        locked_products[item["product"].pk].price * item["quantity"]
        for item in cart_items
    )
    order = Order.objects.create(
        user=user if user and user.is_authenticated else None,
        subtotal=subtotal,
        total=subtotal,
        **cleaned_data,
    )
    for item in cart_items:
        product = locked_products[item["product"].pk]
        line_total = product.price * item["quantity"]
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            unit_price=product.price,
            quantity=item["quantity"],
            line_total=line_total,
        )
        product.stock = max(0, product.stock - item["quantity"])
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
        lines.append(
            f"- {item.quantity} x {item.product_name}: "
            f"{settings.currency} {item.line_total:,}"
        )
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
