from django.shortcuts import render

# Create your views here.
from .forms import FormLogin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from critics.views import flux


def login_view(request):
    form_login = FormLogin()

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)

        if request.user.is_authenticated:
            return redirect(reverse_lazy(flux))

    if request.method == "POST":
        form_login = FormLogin(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data["username"]
            password = form_login.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy(flux))

    context = {"form": form_login}
    return render(request, "account/login.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Inscription réussie !")
            return redirect(reverse_lazy(login_view))
    else:
        form = UserCreationForm()

    return render(request, "account/register.html", {"form": form})


def index(request):
    return redirect(reverse_lazy(login_view))
