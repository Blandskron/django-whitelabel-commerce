from django.urls import path

from apps.catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("categoria/<slug:slug>/", views.category_detail, name="category_detail"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
]
