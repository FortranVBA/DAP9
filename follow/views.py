"""Project OC DAP 9 - Follow views file."""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import FormFollow
from .models import UserFollows
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def get_follow_view(request):
    """Get the follow user view."""
    form_login = FormFollow(prefix="form_login")

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("follow"))

    if request.method == "POST":
        form_follow = FormFollow(request.POST, prefix="form_login")
        if form_follow.is_valid():
            follow_user = form_follow.cleaned_data["followname"]
            message = UserFollows.objects.follow_user(request.user, follow_user)
            messages.add_message(request, messages.INFO, message)

    filter = UserFollows.objects.filter
    following_users = filter(user=request.user)
    followed_by = [follow.user for follow in filter(followed_user=request.user)]

    context = {
        "form_login": form_login,
        "user": request.user,
        "following_users": following_users,
        "followed_by": followed_by,
    }
    return render(request, "follow/follow.html", context)


@login_required
def unfollow_user(request, userfollows):
    """Unfollow user and redirect to the follow user view."""
    userfollows_content = UserFollows.objects.get(pk=userfollows)

    if request.method == "POST":
        if request.user == userfollows_content.user:
            userfollows_content.delete()

            messages.add_message(request, messages.INFO, "Abonnement supprimé.")

    return redirect(reverse_lazy("follow"))
