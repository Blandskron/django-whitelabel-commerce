from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from apps.orders.models import Order


class CustomerLoginView(LoginView):
    template_name = "customers/login.html"


class CustomerLogoutView(LogoutView):
    pass


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("customers:profile")
    else:
        form = UserCreationForm()
    return render(request, "customers/register.html", {"form": form})


def profile(request):
    orders = []
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)[:20]
    return render(request, "customers/profile.html", {"orders": orders})
