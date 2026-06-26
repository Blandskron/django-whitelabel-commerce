# Generated manually for the initial order schema.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(blank=True, max_length=32, unique=True, verbose_name="codigo")),
                ("customer_name", models.CharField(max_length=160, verbose_name="nombre")),
                ("customer_phone", models.CharField(max_length=40, verbose_name="telefono")),
                ("customer_email", models.EmailField(blank=True, max_length=254, verbose_name="email")),
                ("shipping_address", models.CharField(blank=True, max_length=255, verbose_name="direccion")),
                ("customer_note", models.TextField(blank=True, verbose_name="comentario")),
                ("status", models.CharField(choices=[("pending", "Pendiente"), ("confirmed", "Confirmado"), ("preparing", "En preparacion"), ("ready", "Listo"), ("delivered", "Entregado"), ("cancelled", "Cancelado")], default="pending", max_length=24, verbose_name="estado")),
                ("payment_status", models.CharField(choices=[("unpaid", "No pagado"), ("payment_review", "Revision de pago"), ("paid", "Pagado"), ("refunded", "Devuelto"), ("cancelled", "Pago cancelado")], default="unpaid", max_length=24, verbose_name="estado de pago")),
                ("subtotal", models.PositiveIntegerField(default=0, verbose_name="subtotal")),
                ("total", models.PositiveIntegerField(default=0, verbose_name="total")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "pedido",
                "verbose_name_plural": "pedidos",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("product_name", models.CharField(max_length=160, verbose_name="producto")),
                ("unit_price", models.PositiveIntegerField(verbose_name="precio unitario")),
                ("quantity", models.PositiveIntegerField(verbose_name="cantidad")),
                ("line_total", models.PositiveIntegerField(verbose_name="total linea")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")),
                ("product", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="order_items", to="catalog.product")),
            ],
            options={
                "verbose_name": "item de pedido",
                "verbose_name_plural": "items de pedido",
            },
        ),
    ]
