"""Project OC DAP 9 - Ticket forms file."""

from django import forms

from .models import Ticket


class FormCreateTicket(forms.ModelForm):
    """Ticket creation form."""

    class Meta:
        """Form meta properties."""

        model = Ticket
        fields = ["title", "description", "image"]
