"""Project OC DAP 9 - Account forms file."""

from django import forms


class FormLogin(forms.Form):
    """User login form."""

    username = forms.CharField(label=("Nom d'utilisateur"), required=True)
    password = forms.CharField(
        label=("Mot de passe"), required=True, widget=forms.PasswordInput()
    )
