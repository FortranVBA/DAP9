# Create your views here.

from django.views.generic.edit import CreateView, UpdateView
from .forms import FormCreateTicket
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket


class CreateTicket(LoginRequiredMixin, CreateView):

    template_name = "ticket/create_ticket.html"
    form_class = FormCreateTicket
    success_url = reverse_lazy("flux")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):

    model = Ticket
    fields = ["title", "description", "image"]
    success_url = "/"
