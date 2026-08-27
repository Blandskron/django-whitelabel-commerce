from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.common.models import TimeStampedModel


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    CONFIRMED = "confirmed", "Confirmado"
    PREPARING = "preparing", "En preparacion"
    READY = "ready", "Listo"
    DELIVERED = "delivered", "Entregado"
    CANCELLED = "cancelled", "Cancelado"


class PaymentStatus(models.TextChoices):
    UNPAID = "unpaid", "No pagado"
    PAYMENT_REVIEW = "payment_review", "Revision de pago"
    PAID = "paid", "Pagado"
    REFUNDED = "refunded", "Devuelto"
    CANCELLED = "cancelled", "Pago cancelado"


class Order(TimeStampedModel):
    code = models.CharField("codigo", max_length=32, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer_name = models.CharField("nombre", max_length=160)
    customer_phone = models.CharField("telefono", max_length=40)
    customer_email = models.EmailField("email", blank=True)
    shipping_address = models.CharField("direccion", max_length=255, blank=True)
    customer_note = models.TextField("comentario", blank=True)
    status = models.CharField(
        "estado",
        max_length=24,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    payment_status = models.CharField(
        "estado de pago",
        max_length=24,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
    )
    subtotal = models.PositiveIntegerField("subtotal", default=0)
    total = models.PositiveIntegerField("total", default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return self.code or f"Pedido #{self.pk}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.code:
            today = timezone.localdate(self.created_at).strftime("%Y%m%d")
            self.code = f"PED-{today}-{self.pk:06d}"
            super().save(update_fields=["code", "updated_at"])

    def get_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"code": self.code})


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "catalog.Product",
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product_name = models.CharField("producto", max_length=160)
    unit_price = models.PositiveIntegerField("precio unitario")
    quantity = models.PositiveIntegerField("cantidad")
    line_total = models.PositiveIntegerField("total linea")

    class Meta:
        verbose_name = "item de pedido"
        verbose_name_plural = "items de pedido"

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
