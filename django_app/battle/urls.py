from django.conf.urls import patterns, include, url
import views
from battle.views import BattleAppView, PlayerProfileView, NicknameSearchView

urlpatterns = patterns(views,
    url(r'^api/', include('battle.api.urls')),
    url(r'^player/(?P<player_id>[0-9]+)/$', PlayerProfileView.as_view(), name='player-profile'),
    url(r'^player/search/$', NicknameSearchView.as_view(), name='nickname-search'),
    url(r'^$', BattleAppView.as_view(), name='battle-app'),
)
