# Create your views here.
from django.http import HttpResponse

from django.views.generic.edit import CreateView
from django.template import loader

# from .models import User
from django.contrib.auth.models import User
from .forms import FormRegister
from django.urls import reverse


def login(request):
    template = loader.get_template("critics/index.html")
    return HttpResponse(template.render(request=request))


def reg_success(request):
    template = loader.get_template("critics/reg_success.html")
    return HttpResponse(template.render(request=request))


class ViewRegister(CreateView):
    template_name = "critics/register.html"
    form_class = FormRegister
    # model = User
    # fields = ["username"]
    def get_success_url(self):
        return reverse(reg_success)
