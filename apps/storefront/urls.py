from django.urls import path

from apps.storefront import views

app_name = "storefront"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacto/", views.contact, name="contact"),
]
