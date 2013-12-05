from battle.models import Player
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication

class KixeyeResource(ModelResource):
    class Meta:
        always_return_data = True
        # Add it here.
        authentication = BasicAuthentication()
        serializer = Serializer(formats = ['json'])
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put']

class PlayerResource(KixeyeResource):
    class Meta(KixeyeResource.Meta):
        queryset = Player.objects.all()
        resource_name = 'player'

class BattleResource(KixeyeResource):
    attacker = fields.ForeignKey(PlayerResource, 'attacker')
    defender = fields.ForeignKey(PlayerResource, 'defender')
    winner = fields.ForeignKey(PlayerResource, 'winner')

    class Meta(KixeyeResource.Meta):
        queryset = Player.objects.all()
        resource_name = 'battle'
