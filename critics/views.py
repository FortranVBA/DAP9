# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import logout


def flux(request):

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)

    if not request.user.is_authenticated:
        from account.views import login_view

        return redirect(reverse_lazy(login_view))

    context = {"user": request.user}
    return render(request, "critics/flux.html", context)
