from django import forms


class FormFollow(forms.Form):
    followname = forms.CharField(label=("Nom d'utilisateur"), required=True)
