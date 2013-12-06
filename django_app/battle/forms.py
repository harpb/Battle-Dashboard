from battle.models import Player, Battle
from django import forms

class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'nickname']

    def clean_nickname(self):
        """
        Validate that the nickname is not already in use.
        """
        try:
            Player.objects.get(nickname__iexact = self.cleaned_data['nickname'])
        except Player.DoesNotExist:
            return self.cleaned_data['nickname']
        raise forms.ValidationError(u'This nickname is already taken. Please choose another.')

class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
