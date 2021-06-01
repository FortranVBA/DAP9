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
    form_login = FormFollow(prefix="form_login")

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("follow"))

    if request.method == "POST":
        if "form_login" or True in request.POST:
            form_follow = FormFollow(request.POST, prefix="form_login")

            if form_follow.is_valid():
                follow_user = form_follow.cleaned_data["followname"]
                if User.objects.filter(username=follow_user).exists():
                    if str(follow_user) == str(request.user):
                        messages.add_message(request, messages.INFO, "Same user")
                    else:
                        if UserFollows.objects.filter(
                            user=request.user,
                            followed_user=User.objects.get(username=follow_user),
                        ).exists():
                            messages.add_message(
                                request, messages.INFO, "Already followed"
                            )
                        else:
                            messages.add_message(
                                request, messages.INFO, "Follow created"
                            )
                            new_follow = UserFollows(
                                user=request.user,
                                followed_user=User.objects.get(username=follow_user),
                            )
                            new_follow.save()
                else:
                    messages.add_message(request, messages.INFO, "User not found")

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
def unfollow(request, userfollows):

    userfollows_content = UserFollows.objects.get(pk=userfollows)

    if request.method == "POST":
        userfollows_content.delete()

    return redirect(reverse_lazy("follow"))
