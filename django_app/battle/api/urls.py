from tastypie.api import Api
from battle.api.resources import PlayerResource, BattleResource

v1_api = Api(api_name='v1')
v1_api.register(BattleResource())
v1_api.register(PlayerResource())
urlpatterns = v1_api.urls
