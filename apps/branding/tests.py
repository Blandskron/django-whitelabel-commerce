from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.branding.models import StoreSettings


class StoreSettingsTests(TestCase):
    def test_load_creates_one_reusable_configuration(self):
        first = StoreSettings.load()
        second = StoreSettings.load()

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(StoreSettings.objects.count(), 1)

    def test_rejects_a_second_configuration(self):
        StoreSettings.load()

        with self.assertRaises(ValidationError):
            StoreSettings(store_name="Otra tienda").full_clean()
