from django.core.management.base import BaseCommand

from apps.branding.models import StoreSettings
from apps.catalog.models import Category, Product


DEMO_CATALOG = (
    {
        "category": {
            "name": "Accesorios",
            "description": "Objetos utiles para el dia a dia.",
            "sort_order": 10,
        },
        "products": (
            {
                "name": "Botella reutilizable",
                "price": 12990,
                "stock": 20,
                "is_featured": True,
            },
            {
                "name": "Bolso urbano",
                "price": 24990,
                "stock": 12,
                "is_featured": True,
            },
        ),
    },
    {
        "category": {
            "name": "Hogar",
            "description": "Productos simples para espacios cotidianos.",
            "sort_order": 20,
        },
        "products": (
            {
                "name": "Vela aromatica",
                "price": 8990,
                "stock": 30,
                "is_featured": True,
            },
            {
                "name": "Taza de ceramica",
                "price": 10990,
                "stock": 18,
                "is_featured": False,
            },
        ),
    },
)


class Command(BaseCommand):
    help = "Carga un catalogo demostrativo de forma idempotente."

    def handle(self, *args, **options):
        StoreSettings.load()
        created_categories = 0
        created_products = 0

        for entry in DEMO_CATALOG:
            category_defaults = entry["category"].copy()
            category_name = category_defaults.pop("name")
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults=category_defaults,
            )
            created_categories += int(created)

            for product_data in entry["products"]:
                product_defaults = product_data.copy()
                product_name = product_defaults.pop("name")
                _, created = Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        **product_defaults,
                        "short_description": (
                            "Producto de demostracion para explorar el flujo de compra."
                        ),
                    },
                )
                created_products += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed listo: {created_categories} categorias y "
                f"{created_products} productos nuevos."
            )
        )
