from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.common.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField("nombre", max_length=120, unique=True)
    slug = models.SlugField("slug", max_length=140, unique=True, blank=True)
    description = models.TextField("descripcion", blank=True)
    is_active = models.BooleanField("activa", default=True)
    sort_order = models.PositiveIntegerField("orden", default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        verbose_name="categoria",
        related_name="products",
        on_delete=models.PROTECT,
    )
    name = models.CharField("nombre", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    short_description = models.CharField("descripcion corta", max_length=220, blank=True)
    description = models.TextField("descripcion", blank=True)
    main_image = models.ImageField("imagen principal", upload_to="products/", blank=True)
    price = models.PositiveIntegerField("precio")
    stock = models.PositiveIntegerField("stock", default=0)
    is_active = models.BooleanField("activo", default=True)
    is_featured = models.BooleanField("destacado", default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def is_available(self):
        return self.is_active and self.stock > 0


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField("imagen", upload_to="products/gallery/")
    alt_text = models.CharField("texto alternativo", max_length=160, blank=True)
    sort_order = models.PositiveIntegerField("orden", default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "imagen de producto"
        verbose_name_plural = "imagenes de producto"

    def __str__(self):
        return self.alt_text or f"Imagen de {self.product}"
