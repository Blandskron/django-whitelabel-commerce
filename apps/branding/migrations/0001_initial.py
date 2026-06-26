# Generated manually for the initial white label store configuration.

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StoreSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("store_name", models.CharField(default="Tienda Aurora", max_length=120, verbose_name="nombre de tienda")),
                ("logo", models.ImageField(blank=True, upload_to="stores/logos/", verbose_name="logo")),
                ("favicon", models.ImageField(blank=True, upload_to="stores/favicons/", verbose_name="favicon")),
                ("primary_color", models.CharField(default="#0f766e", max_length=7, verbose_name="color principal")),
                ("secondary_color", models.CharField(default="#f59e0b", max_length=7, verbose_name="color secundario")),
                ("hero_title", models.CharField(default="Compra facil por WhatsApp", max_length=160, verbose_name="titulo hero")),
                ("hero_subtitle", models.TextField(default="Productos seleccionados, pedido rapido y pago por transferencia.", verbose_name="subtitulo hero")),
                ("whatsapp_number", models.CharField(blank=True, max_length=32, verbose_name="WhatsApp de ventas")),
                ("contact_email", models.EmailField(blank=True, max_length=254, verbose_name="email de contacto")),
                ("instagram_url", models.URLField(blank=True, verbose_name="Instagram")),
                ("facebook_url", models.URLField(blank=True, verbose_name="Facebook")),
                ("address", models.CharField(blank=True, max_length=255, verbose_name="direccion")),
                ("bank_details", models.TextField(blank=True, verbose_name="datos bancarios")),
                ("currency", models.CharField(default="CLP", max_length=8, verbose_name="moneda")),
                ("show_stock", models.BooleanField(default=True, verbose_name="mostrar stock")),
                ("allow_out_of_stock_orders", models.BooleanField(default=False, verbose_name="permitir pedido sin stock")),
                ("maintenance_mode", models.BooleanField(default=False, verbose_name="modo mantenimiento")),
            ],
            options={
                "verbose_name": "configuracion de tienda",
                "verbose_name_plural": "configuracion de tienda",
            },
        ),
    ]
