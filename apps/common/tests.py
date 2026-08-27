from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.catalog.models import Category, Product


class EducationalCommandsTests(TestCase):
    def test_seed_demo_is_idempotent(self):
        call_command("seed_demo", verbosity=0)
        first_counts = (Category.objects.count(), Product.objects.count())

        call_command("seed_demo", verbosity=0)

        self.assertEqual(first_counts, (2, 4))
        self.assertEqual(
            (Category.objects.count(), Product.objects.count()),
            first_counts,
        )

    @patch.dict(
        "os.environ",
        {
            "DJANGO_SUPERUSER_USERNAME": "admin",
            "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "educational-password",
        },
    )
    def test_ensure_superuser_is_idempotent(self):
        call_command("ensure_superuser", verbosity=0)
        call_command("ensure_superuser", verbosity=0)

        user = get_user_model().objects.get(username="admin")
        self.assertTrue(user.is_superuser)
        self.assertEqual(get_user_model().objects.count(), 1)
