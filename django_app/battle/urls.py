from django.conf.urls import patterns, include, url
import views
from battle.views import BattleAppView
urlpatterns = patterns(views,
    url(r'^api/', include('battle.api.urls')),
    url(r'^$', BattleAppView.as_view(), name='battle-app'),
)
