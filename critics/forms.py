from django import forms

from ticket.models import Ticket
from .models import Review


class FormCreateTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class FormCreateReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
