from battle.models import Player, Battle
from tastypie import fields
from tastypie.constants import ALL
from battle.forms import PlayerForm, BattleForm
from utilities.tastypie_helper import FormSaveValidation, KixeyeResource

class PlayerResource(KixeyeResource):
    class Meta(KixeyeResource.Meta):
        queryset = Player.objects.all()
        resource_name = 'player'
        filtering = {
            'nickname': ALL
        }
        validation = FormSaveValidation(form_class = PlayerForm)

class BattleResource(KixeyeResource):
    attacker = fields.ForeignKey(PlayerResource, 'attacker', full = True)
    defender = fields.ForeignKey(PlayerResource, 'defender', full = True)
    winner = fields.ForeignKey(PlayerResource, 'winner')

    class Meta(KixeyeResource.Meta):
        queryset = Battle.objects.all()
        resource_name = 'battle'
        filtering = {
            'start': ALL,
            'end': ALL
        }
        validation = FormSaveValidation(form_class = BattleForm)
