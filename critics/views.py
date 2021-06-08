"""Project OC DAP 9 - Critics views file."""

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from itertools import chain
from ticket.models import Ticket
from .models import Review
from .forms import FormCreateTicket, FormCreateReview
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def get_flux_view(request):
    """Get the flux view."""
    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("flux"))

    context = {"user": request.user}

    # Get tickets to be included
    tickets = Ticket.objects.get_user_flux(request.user)

    # Get reviews to be included
    reviews = Review.objects.get_user_flux(request.user)

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    context["posts"] = posts

    return render(request, "critics/flux.html", context)


@login_required
def create_review(request):
    """Get the review creation view."""
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
        ticket_form = FormCreateTicket(request.POST, request.FILES)
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
    """Get the review created as ticket reply view."""
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
def get_myposts_view(request):
    """Get the user posts view."""
    if request.method == "GET":
        if "action" in request.GET:
            action = request.GET.get("action")
            if action == "logout":
                if request.user.is_authenticated:
                    logout(request)
                    return redirect(reverse_lazy("flux"))

    context = {"user": request.user}

    tickets = Ticket.objects.get_by_user(request.user)
    reviews = Review.objects.get_by_user(request.user)

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    context["posts"] = posts

    return render(request, "critics/your_posts.html", context)


@login_required
def delete_review(request, review):
    """Delete the review and redirect to the user posts view."""
    review_content = Review.objects.get(pk=review)

    if request.method == "POST":
        if request.user == review_content.user:
            review_content.delete()

    return redirect(reverse_lazy("myposts"))


@login_required
def delete_ticket(request, ticket):
    """Delete the ticket and redirect to the user posts view."""
    ticket_content = Ticket.objects.get(pk=ticket)

    if request.method == "POST":
        if request.user == ticket_content.user:
            ticket_content.delete()

    return redirect(reverse_lazy("myposts"))


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Get the review update view."""

    model = Review
    success_url = "/"
    form_class = FormCreateReview

    def get_context_data(self, **kwargs):
        """Add the ticket object to the context."""
        context = super().get_context_data(**kwargs)

        context["ticket"] = self.get_object().ticket

        return context
