from django import forms

class CreatePlayerForm(forms.Form):
    name = forms.CharField(max_length = 50, label = 'Neuer Spieler')

##class linkPlayer(forms.Form):

##    Spieler = forms.
