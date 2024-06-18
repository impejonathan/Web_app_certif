# authentication/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
    


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        
        


class PredictionForm(forms.Form):
    Descriptif = forms.CharField(max_length=100)
    Note = forms.CharField(max_length=10)
    Marque = forms.CharField(max_length=50)
    Consommation = forms.CharField(max_length=10)
    Indice_Pluie = forms.CharField(max_length=10)
    Bruit = forms.IntegerField()
    Saisonalite = forms.CharField(max_length=20)
    Type_Vehicule = forms.CharField(max_length=50)
    Runflat = forms.CharField(max_length=10)
    Largeur = forms.IntegerField()
    Hauteur = forms.IntegerField()
    Diametre = forms.IntegerField()
    Charge = forms.IntegerField()
    Vitesse = forms.CharField(max_length=10)