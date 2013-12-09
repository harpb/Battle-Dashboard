from tastypie.resources import Resource, ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.serializers import Serializer
from tastypie.validation import Validation, CleanedDataFormValidation
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
import json
from tastypie.authentication import SessionAuthentication
import logging
from django.forms.models import model_to_dict
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model
User = get_user_model()

from tastypie.authentication import BasicAuthentication

class KixeyeResource(ModelResource):
    class Meta:
        always_return_data = True
        authentication = BasicAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats = ['json'])
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put']
        max_limit = 100
        limit = max_limit

    def _handle_500(self, request, exception):
        logger.exception(str(exception))
        return super(KixeyeResource, self)._handle_500(request, exception)

    def obj_create(self, bundle, **kwargs):
        self._meta.validation.save(bundle, bundle.request)
        return bundle

#===============================================================================
# Validation
#===============================================================================
class FormValidationErrors(Exception):
    pass

class FormSaveValidation(CleanedDataFormValidation):

    def save(self, bundle, request = None):
        """
        Checks ``bundle.data``to ensure it is valid & replaces it with the
        cleaned results.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """
#         bundle.data['user'] = request.user.id
#         logger.info('bundle.data: %r', bundle.data)
        form = self.form_class(**self.form_args(bundle))

        if not form.is_valid():
            # The data is invalid. Let's collect all the error messages & raise exception.
            error_list = {key: [item for item in value] for key, value in form.errors.items()}
            response = HttpBadRequest(content = json.dumps(error_list))
            raise ImmediateHttpResponse(response)

        # We're different here & relying on having a reference to the same
        # bundle the rest of the process is using.
        bundle.data = form.cleaned_data
#         logger.info('bundle: %r %r %r %r', bundle, form.instance, model_to_dict(form.instance))
        bundle.obj = form.save()