from battle.models import Player, Battle
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication
from tastypie.constants import ALL
from tastypie.authorization import Authorization

class KixeyeResource(ModelResource):
    class Meta:
        always_return_data = True
        # Add it here.
        authentication = BasicAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats = ['json'])
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put']

class PlayerResource(KixeyeResource):
    class Meta(KixeyeResource.Meta):
        queryset = Player.objects.all()
        resource_name = 'player'
        filtering = {
            'nickname': ALL
        }

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
