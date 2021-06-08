"""Project OC DAP 9 - Follow forms file."""

from django import forms


class FormFollow(forms.Form):
    """Follow user form."""

    followname = forms.CharField(label=("Nom d'utilisateur"), required=True)
