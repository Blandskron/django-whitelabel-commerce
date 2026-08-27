from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Accesorios")
        cls.product = Product.objects.create(
            category=cls.category,
            name="Bolso urbano",
            price=24990,
            stock=4,
        )

    def test_models_generate_slugs_and_absolute_urls(self):
        self.assertEqual(self.category.slug, "accesorios")
        self.assertEqual(self.product.slug, "bolso-urbano")
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse("catalog:product_detail", kwargs={"slug": "bolso-urbano"}),
        )

    def test_product_list_only_shows_active_products(self):
        inactive = Product.objects.create(
            category=self.category,
            name="Producto oculto",
            price=1000,
            stock=1,
            is_active=False,
        )

        response = self.client.get(reverse("catalog:product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, inactive.name)

    def test_product_detail_returns_404_for_inactive_product(self):
        self.product.is_active = False
        self.product.save(update_fields=["is_active", "updated_at"])

        response = self.client.get(self.product.get_absolute_url())

        self.assertEqual(response.status_code, 404)
