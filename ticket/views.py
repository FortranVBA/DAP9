from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.generic.edit import CreateView
from .forms import FormCreateTicket
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from critics.views import flux


class CreateTicket(CreateView):

    template_name = "ticket/create_ticket.html"
    form_class = FormCreateTicket
    success_url = reverse_lazy(flux)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_user = ""

        if "username" in self.request.session:
            active_user = self.request.session["username"]

        context["user"] = active_user

        return context

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        return HttpResponseRedirect(self.get_success_url())


# class ViewRegister(SuccessMessageMixin, CreateView):
#    template_name = "critics/register.html"
#    form_class = FormRegister
#    success_message = "Inscription réussie ! Veillez vous connecter."
#    success_url = reverse_lazy(login)
