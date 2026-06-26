from django.urls import path

from apps.orders import views

app_name = "orders"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("pedido/<str:code>/", views.order_detail, name="order_detail"),
]
