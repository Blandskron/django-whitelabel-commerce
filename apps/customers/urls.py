from django.urls import path

from apps.customers import views

app_name = "customers"

urlpatterns = [
    path("login/", views.CustomerLoginView.as_view(), name="login"),
    path("logout/", views.CustomerLogoutView.as_view(), name="logout"),
    path("registro/", views.register, name="register"),
    path("perfil/", views.profile, name="profile"),
]
