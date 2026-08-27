from django.test import TestCase
from django.urls import reverse


class StorefrontSmokeTests(TestCase):
    def test_public_pages_render(self):
        for url_name in ("storefront:home", "storefront:contact"):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
