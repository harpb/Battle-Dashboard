from tastypie.api import Api

api = Api(api_name='v1')
urlpatterns = api.urls
