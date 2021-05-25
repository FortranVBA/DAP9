from django import forms


class FormLogin(forms.Form):
    username = forms.CharField(label=("Nom d'utilisateur"), required=True)
    password = forms.CharField(label=("Mot de passe"), required=True)
