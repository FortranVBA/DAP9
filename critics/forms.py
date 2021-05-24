from django import forms

from django.contrib.auth.models import User


class FormLogin(forms.Form):
    username = forms.CharField(label=("Nom d'utilisateur"), required=True)
    password = forms.CharField(label=("Mot de passe"), required=True)
