from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.branding.models import StoreSettings
from apps.catalog.models import Category, Product
from apps.orders.models import Order


CHECKOUT_DATA = {
    "customer_name": "Ada Lovelace",
    "customer_phone": "+56 9 1111 2222",
    "customer_email": "ada@example.com",
    "shipping_address": "Calle Educativa 123",
    "customer_note": "Entregar por la tarde",
}


class CheckoutTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Accesorios")
        self.product = Product.objects.create(
            category=category,
            name="Botella",
            price=10000,
            stock=3,
        )

    def add_product_to_session(self, quantity=1):
        session = self.client.session
        session["cart"] = {str(self.product.pk): quantity}
        session.save()

    def test_checkout_creates_order_decrements_stock_and_remembers_guest(self):
        self.add_product_to_session(quantity=2)

        response = self.client.post(reverse("orders:checkout"), CHECKOUT_DATA)

        order = Order.objects.get()
        self.assertRedirects(response, order.get_absolute_url())
        self.assertEqual(order.total, 20000)
        self.assertEqual(order.items.get().product_name, "Botella")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(self.client.get(order.get_absolute_url()).status_code, 200)

    def test_order_detail_is_hidden_from_a_different_guest_session(self):
        self.add_product_to_session()
        self.client.post(reverse("orders:checkout"), CHECKOUT_DATA)
        order = Order.objects.get()

        other_client_response = self.client_class().get(order.get_absolute_url())

        self.assertEqual(other_client_response.status_code, 404)

    def test_checkout_rechecks_stock_before_creating_order(self):
        self.add_product_to_session(quantity=2)
        self.product.stock = 1
        self.product.save(update_fields=["stock", "updated_at"])

        response = self.client.post(reverse("orders:checkout"), CHECKOUT_DATA)

        self.assertRedirects(response, reverse("cart:detail"))
        self.assertFalse(Order.objects.exists())
        self.assertIn("cart", self.client.session)

    def test_store_can_explicitly_allow_an_order_above_stock(self):
        store_settings = StoreSettings.load()
        store_settings.allow_out_of_stock_orders = True
        store_settings.save()
        self.add_product_to_session(quantity=5)

        response = self.client.post(reverse("orders:checkout"), CHECKOUT_DATA)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get().items.get().quantity, 5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 0)

    def test_authenticated_owner_can_reopen_order_without_guest_session(self):
        user = get_user_model().objects.create_user("ada", password="safe-password")
        order = Order.objects.create(
            user=user,
            customer_name="Ada",
            customer_phone="123",
            subtotal=0,
            total=0,
        )
        self.client.force_login(user)

        response = self.client.get(order.get_absolute_url())

        self.assertEqual(response.status_code, 200)
