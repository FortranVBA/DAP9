from django import forms

from .models import Ticket


class FormCreateTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
