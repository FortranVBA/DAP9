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
from .models import Review
from django.db.models import Subquery
from django.contrib import messages
from .forms import FormCreateTicket, FormCreateReview
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


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

    # Get tickets to be included
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

    # Get reviews to be included
    reviews_by_user = Review.objects.filter(user=request.user)
    reviews_by_user = reviews_by_user.annotate(
        content_type=Value("REVIEW", CharField())
    )

    reviews_by_followed_users = Review.objects.filter(
        user__in=Subquery(users_followed.values("followed_user"))
    )
    reviews_by_followed_users = reviews_by_followed_users.annotate(
        content_type=Value("REVIEW", CharField())
    )

    reviews_reply = Review.objects.filter(
        ticket__in=Subquery(tickets_by_user.values("id"))
    )
    reviews_reply = reviews_reply.annotate(content_type=Value("REVIEW", CharField()))

    reviews = reviews_by_user.union(reviews_by_followed_users)
    reviews = reviews.union(reviews_reply)

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

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


@login_required
def reply_review(request, ticket):

    form_review = FormCreateReview()
    ticket_content = Ticket.objects.get(pk=ticket)

    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("flux"))

    if request.method == "POST":
        form_review = FormCreateReview(request.POST)
        if form_review.is_valid():
            form_review.instance.user = request.user
            form_review.instance.ticket = ticket_content
            form_review.save()
            return redirect(reverse_lazy("flux"))

    return render(
        request,
        "critics/reply_review.html",
        {"ticket_content": ticket_content, "form_review": form_review},
    )


@login_required
def myposts(request):

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
    tickets = tickets_by_user

    reviews_by_user = Review.objects.filter(user=request.user)
    reviews_by_user = reviews_by_user.annotate(
        content_type=Value("REVIEW", CharField())
    )
    reviews = reviews_by_user

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    context["posts"] = posts

    return render(request, "critics/your_posts.html", context)


@login_required
def review_delete(request, review):

    review_content = Review.objects.get(pk=review)

    if request.method == "POST":
        review_content.delete()

    return redirect(reverse_lazy("myposts"))


@login_required
def ticket_delete(request, ticket):

    ticket_content = Ticket.objects.get(pk=ticket)

    if request.method == "POST":
        ticket_content.delete()

    return redirect(reverse_lazy("myposts"))


class ReviewUpdateView(LoginRequiredMixin, UpdateView):

    model = Review
    fields = ["headline", "rating", "body"]
    success_url = "/"
