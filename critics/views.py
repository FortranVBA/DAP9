# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render


def flux(request):
    active_user = ""

    if "username" in request.session:
        active_user = request.session["username"]

    if not active_user:
        from account.views import login

        return redirect(reverse_lazy(login))

    context = {"user": active_user}
    return render(request, "critics/flux.html", context)
