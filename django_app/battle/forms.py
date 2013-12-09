from battle.models import Player, Battle
from django import forms

class PlayerForm(forms.ModelForm):
    NICKNAME_TAKEN_ERROR = u'This nickname is already taken. Please choose another.'

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
        raise forms.ValidationError(self.NICKNAME_TAKEN_ERROR)

class BattleForm(forms.ModelForm):
    PlAYER_DOES_NOT_EXIST = u'This player does not exists.'
    WINNER_NOT_A_PLAYER = u'Winner must be an attacker or a defender.'
    END_IS_BEFORE_START = u'End datetime must be at or after start datetime.'
    PLAYERS_ERROR = 'Error with attacker or defender data.'

#     def clean_attacker(self):
#         """
#         Validate that the attacker is an existing player's instance.
#         """
#         try:
#             Player.objects.get(attacker = self.cleaned_data['attacker'])
#         except Player.DoesNotExist:
#             raise forms.ValidationError(self.PlAYER_DOES_NOT_EXIST)
#         return self.cleaned_data['attacker']

    def clean_winner(self):
        """
        Validate that the winner is a player involved in the battle.
        """
        winner = self.cleaned_data['winner']
        try:
            if winner != self.cleaned_data['attacker']\
                    and winner != self.cleaned_data['defender']:
                raise forms.ValidationError(self.WINNER_NOT_A_PLAYER)
        except KeyError:
            raise forms.ValidationError(self.PLAYERS_ERROR)

        return winner

    def clean_end(self):
        """
        Validate that the winner is a player involved in the battle.
        """
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if start and end and start > end:
            raise forms.ValidationError(self.END_IS_BEFORE_START)

        return end

    class Meta:
        model = Battle
        fields = ['attacker', 'defender', 'winner', 'start', 'end']
