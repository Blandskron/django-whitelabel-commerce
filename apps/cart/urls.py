from django.urls import path

from apps.cart import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("agregar/<int:product_id>/", views.add_to_cart, name="add"),
    path("actualizar/<int:product_id>/", views.update_cart, name="update"),
    path("remover/<int:product_id>/", views.remove_from_cart, name="remove"),
    path("vaciar/", views.clear_cart, name="clear"),
]
