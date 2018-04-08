from django import forms
from django.forms import ModelForm
from Spielerverwaltung.models import Raid

class CreatePlayerForm(forms.Form):
    name = forms.CharField(max_length = 50, label = 'Neuer Spieler')

class CreateRaidForm(ModelForm):
    class Meta:
        model = Raid
        fields = ['Raidstart','Raidende','Teilnehmer']
        widgets = {
            'Raidstart' : forms.DateTimeInput(attrs= {'type' : 'datetime-local'}),
            'Raidende'  : forms.DateTimeInput(attrs= {'type' : 'datetime-local'})
        }

##class linkPlayer(forms.Form):

##    Spieler = forms.
