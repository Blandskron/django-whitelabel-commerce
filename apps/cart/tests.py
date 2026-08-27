from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product


class CartViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Hogar")
        cls.product = Product.objects.create(
            category=category,
            name="Taza",
            price=4990,
            stock=2,
        )

    def test_adds_a_valid_quantity_to_the_session(self):
        response = self.client.post(
            reverse("cart:add", args=[self.product.pk]),
            {"quantity": 2},
        )

        self.assertRedirects(response, self.product.get_absolute_url())
        self.assertEqual(self.client.session["cart"][str(self.product.pk)], 2)

    def test_rejects_malformed_quantity_without_server_error(self):
        response = self.client.post(
            reverse("cart:add", args=[self.product.pk]),
            {"quantity": "no-es-un-numero"},
        )

        self.assertRedirects(response, self.product.get_absolute_url())
        self.assertNotIn("cart", self.client.session)

    def test_rejects_quantity_above_stock(self):
        response = self.client.post(
            reverse("cart:add", args=[self.product.pk]),
            {"quantity": 3},
        )

        self.assertRedirects(response, self.product.get_absolute_url())
        self.assertNotIn("cart", self.client.session)

    def test_does_not_redirect_to_an_external_next_url(self):
        response = self.client.post(
            reverse("cart:add", args=[self.product.pk]),
            {"quantity": 1, "next": "https://example.org/phishing"},
        )

        self.assertRedirects(response, self.product.get_absolute_url())
