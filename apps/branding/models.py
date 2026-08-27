from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import TimeStampedModel


class StoreSettings(TimeStampedModel):
    store_name = models.CharField("nombre de tienda", max_length=120, default="Tienda Aurora")
    logo = models.ImageField("logo", upload_to="stores/logos/", blank=True)
    favicon = models.ImageField("favicon", upload_to="stores/favicons/", blank=True)
    primary_color = models.CharField("color principal", max_length=7, default="#0f766e")
    secondary_color = models.CharField("color secundario", max_length=7, default="#f59e0b")
    hero_title = models.CharField("titulo hero", max_length=160, default="Compra facil por WhatsApp")
    hero_subtitle = models.TextField(
        "subtitulo hero",
        default="Productos seleccionados, pedido rapido y pago por transferencia.",
    )
    whatsapp_number = models.CharField("WhatsApp de ventas", max_length=32, blank=True)
    contact_email = models.EmailField("email de contacto", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    facebook_url = models.URLField("Facebook", blank=True)
    address = models.CharField("direccion", max_length=255, blank=True)
    bank_details = models.TextField("datos bancarios", blank=True)
    currency = models.CharField("moneda", max_length=8, default="CLP")
    show_stock = models.BooleanField("mostrar stock", default=True)
    allow_out_of_stock_orders = models.BooleanField("permitir pedido sin stock", default=False)
    maintenance_mode = models.BooleanField("modo mantenimiento", default=False)

    class Meta:
        verbose_name = "configuracion de tienda"
        verbose_name_plural = "configuracion de tienda"

    def __str__(self):
        return self.store_name

    def clean(self):
        if not self.pk and StoreSettings.objects.exists():
            raise ValidationError("Solo puede existir una configuracion de tienda.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings
