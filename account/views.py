from django.shortcuts import render

# Create your views here.
from .forms import FormLogin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from critics.views import flux


def login(request):
    form_login = FormLogin()
    active_user = None

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if "username" in request.session:
                    request.session.flush()
                    active_user = None

        if "username" in request.session:
            active_user = request.session["username"]

    if request.method == "POST":
        form_login = FormLogin(request.POST)
        if form_login.is_valid():
            active_user = form_login.cleaned_data["username"]
            password = form_login.cleaned_data["password"]
            user_authen = authenticate(request, username=active_user, password=password)

            if user_authen is not None:
                request.session["username"] = active_user
                return redirect(reverse_lazy(flux))
            else:
                active_user = None

    context = {"form": form_login, "user": active_user}
    return render(request, "account/index.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Inscription réussie !")
            return redirect(reverse_lazy(login))
    else:
        form = UserCreationForm()

    return render(request, "account/register.html", {"form": form})


# class ViewRegister(SuccessMessageMixin, CreateView):
#    template_name = "critics/register.html"
#    form_class = FormRegister
#    success_message = "Inscription réussie ! Veillez vous connecter."
#    success_url = reverse_lazy(login)
