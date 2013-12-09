from django.conf.urls import patterns, include, url
import views
from battle.views import BattleAppView, PlayerProfileView

urlpatterns = patterns(views,
    url(r'^api/', include('battle.api.urls')),
    url(r'^player/(?P<player_id>[0-9]+)/$', PlayerProfileView.as_view(), name='player-profile'),
    url(r'^$', BattleAppView.as_view(), name='battle-app'),
)
