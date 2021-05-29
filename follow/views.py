from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import FormFollow
from .models import UserFollows
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def follow(request):
    form_login = FormFollow()

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("follow"))

    if request.method == "POST":
        form_follow = FormFollow(request.POST)
        if form_follow.is_valid():
            follow_user = form_follow.cleaned_data["followname"]
            if User.objects.filter(username=follow_user).exists():
                if follow_user == request.user:
                    messages.add_message(request, messages.INFO, "Same user")
                else:
                    if UserFollows.objects.filter(
                        user=request.user,
                        followed_user=User.objects.get(username=follow_user),
                    ).exists():
                        messages.add_message(request, messages.INFO, "Already followed")
                    else:
                        messages.add_message(request, messages.INFO, "Follow created")
                        new_follow = UserFollows(
                            user=request.user,
                            followed_user=User.objects.get(username=follow_user),
                        )
                        new_follow.save()
            else:
                messages.add_message(request, messages.INFO, "User not found")

    filter = UserFollows.objects.filter
    following_users = [follow.followed_user for follow in filter(user=request.user)]
    followed_by = [follow.user for follow in filter(followed_user=request.user)]

    context = {
        "form": form_login,
        "user": request.user,
        "following_users": following_users,
        "followed_by": followed_by,
    }
    return render(request, "follow/follow.html", context)
