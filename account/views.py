"""Project OC DAP 9 - Account views file."""

from django.shortcuts import render

# Create your views here.
from .forms import FormLogin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


def get_login_view(request):
    """Get the user login view."""
    form_login = FormLogin()

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)

        if request.user.is_authenticated:
            return redirect(reverse_lazy("flux"))

    if request.method == "POST":
        form_login = FormLogin(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data["username"]
            password = form_login.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("flux"))
            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Nom / mot de passe incorrect",
                )

    context = {"form": form_login}
    return render(request, "account/login.html", context)


def register_user(request):
    """Get the user register view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.INFO,
                "Inscription réussie ! Vous pouvez vous connecter.",
            )
            return redirect(reverse_lazy("login"))
    else:
        form = UserCreationForm()

    return render(request, "account/register.html", {"form": form})


def get_index(request):
    """Get the default main view."""
    return redirect(reverse_lazy("login"))
