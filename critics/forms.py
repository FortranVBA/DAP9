"""Project OC DAP 9 - Critics forms file."""

from django import forms

from ticket.models import Ticket
from .models import Review


class FormCreateTicket(forms.ModelForm):
    """Ticket creation form."""

    class Meta:
        """Form meta properties."""

        model = Ticket
        fields = ["title", "description", "image"]
        labels = {"title": "Titre", "description": "Description", "image": "Image"}


class FormCreateReview(forms.ModelForm):
    """Review creation form."""

    CHOICES = [("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label="Note")

    class Meta:
        """Form meta properties."""

        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre", "body": "Commentaires"}
