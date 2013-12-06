from battle.models import Player, Battle
from django import forms

class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'nickname']

class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
