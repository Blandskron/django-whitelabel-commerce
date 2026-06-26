# Generated manually for the initial catalog schema.

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="nombre")),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True, verbose_name="slug")),
                ("description", models.TextField(blank=True, verbose_name="descripcion")),
                ("is_active", models.BooleanField(default=True, verbose_name="activa")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="orden")),
            ],
            options={
                "verbose_name": "categoria",
                "verbose_name_plural": "categorias",
                "ordering": ["sort_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160, verbose_name="nombre")),
                ("slug", models.SlugField(blank=True, max_length=180, unique=True, verbose_name="slug")),
                ("short_description", models.CharField(blank=True, max_length=220, verbose_name="descripcion corta")),
                ("description", models.TextField(blank=True, verbose_name="descripcion")),
                ("main_image", models.ImageField(blank=True, upload_to="products/", verbose_name="imagen principal")),
                ("price", models.PositiveIntegerField(verbose_name="precio")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="stock")),
                ("is_active", models.BooleanField(default=True, verbose_name="activo")),
                ("is_featured", models.BooleanField(default=False, verbose_name="destacado")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="catalog.category", verbose_name="categoria")),
            ],
            options={
                "verbose_name": "producto",
                "verbose_name_plural": "productos",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("image", models.ImageField(upload_to="products/gallery/", verbose_name="imagen")),
                ("alt_text", models.CharField(blank=True, max_length=160, verbose_name="texto alternativo")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="orden")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="catalog.product")),
            ],
            options={
                "verbose_name": "imagen de producto",
                "verbose_name_plural": "imagenes de producto",
                "ordering": ["sort_order", "id"],
            },
        ),
    ]
