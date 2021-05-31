# Create your views here.

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from itertools import chain
from django.db.models import CharField, Value
from ticket.models import Ticket
from follow.models import UserFollows
from django.contrib.auth.models import User
from django.db.models import Subquery
from django.contrib import messages
from .forms import FormCreateTicket, FormCreateReview


@login_required
def flux(request):

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("flux"))

    context = {"user": request.user}

    tickets_by_user = Ticket.objects.filter(user=request.user)
    tickets_by_user = tickets_by_user.annotate(
        content_type=Value("TICKET", CharField())
    )

    users_followed = UserFollows.objects.filter(user=request.user)
    tickets_by_followed_users = Ticket.objects.filter(
        user__in=Subquery(users_followed.values("followed_user"))
    )
    tickets_by_followed_users = tickets_by_followed_users.annotate(
        content_type=Value("TICKET", CharField())
    )
    tickets = tickets_by_user.union(tickets_by_followed_users)

    # returns queryset of tickets

    # combine and sort the two types of posts
    # posts = sorted(
    #    chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    # )
    posts = tickets

    messages.add_message(request, messages.INFO, "Debug message")

    context["posts"] = posts

    return render(request, "critics/flux.html", context)


@login_required
def create_review(request):

    form_ticket = FormCreateTicket()
    form_review = FormCreateReview()

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("flux"))

    if request.method == "POST":
        ticket_form = FormCreateTicket(request.POST)
        review_form = FormCreateReview(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket_form.instance.user = request.user
            ticket = ticket_form.save()

            review_form.instance.user = request.user
            review_form.instance.ticket = ticket
            review_form.save()
            return redirect(reverse_lazy("flux"))

    return render(
        request,
        "critics/create_review.html",
        {"form_ticket": form_ticket, "form_review": form_review},
    )
