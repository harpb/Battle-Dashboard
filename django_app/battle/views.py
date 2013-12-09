from django.views.generic.base import TemplateView
from battle.models import Battle, Player
from django.db.models import Q

class BattleAppView(TemplateView):
    template_name = 'battle-app.html'

class PlayerProfileView(TemplateView):
    template_name = 'player-profile.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerProfileView, self).get_context_data(**kwargs)
        player_id = self.kwargs.get('player_id')
        context['battles'] = Battle.objects.filter(Q(attacker = player_id) | Q(defender = player_id))
        context['player'] = Player.objects.get(id = player_id)
        context['title'] = '%s\'s Profile' % context['player'].nickname 
        return context
