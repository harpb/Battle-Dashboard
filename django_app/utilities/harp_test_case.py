import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
from tastypie.test import TestApiClient, ResourceTestCase
from django.conf import settings
from types import DictType, ListType
import json

class HarpTestCase(ResourceTestCase):

    RESOURCES_PATH = '%s/static/tests_resources' % settings.BASE_DIR
    PATHS = {
        'battle': '/api/v1/battle/',
        'player': '/api/v1/player/'
    }
    TASTYPIE_CLIENT = TestApiClient()
    username = 'harp'
    password = 'great'
    fixtures = [
        'auth_user.json',
        'players.json',
        'battles.json'
    ]
    user_id = 1

    def assertEmpty(self, instance):
        self.assertEqual(len(instance), 0)

    def assertNone(self, instance):
        self.assertEqual(instance, None)

    def assertEqualDict(self, actual, expected):
        for key in expected:
            if isinstance(expected[key], DictType):
                self.assertEqualDict(self, actual[key], expected[key])
            else:
                self.assertEqual(actual[key], expected[key])

        self.assertEqual(len(actual), len(expected))

    def assertHttpAuthorized(self, resp):
        """
        Ensures the response is returning a HTTP 200.
        """
        return self.assertEqual(resp.status_code, 200)

    @classmethod
    def print_json(cls, output = None):
        if not output:
            output = cls.output
        if not (isinstance(output, DictType) or isinstance(output, ListType)):
            output = json.loads(output)

        print json.dumps(output, sort_keys = True, indent = 4)
        return output

    def json_to_dict(self, content = None):
        return json.loads(content)

    @classmethod
    def run_tests(cls, module_name, test_class_name, test_methods, verbose = False, fail_fast = True):
        if module_name is None:
            raise Exception("Where's the module name, eh?")

        import sys
        tests = []
        if test_methods:
            tests = ["%s.%s.%s" % (module_name, test_class_name, test_method)
                    for test_method in test_methods]
        else:
            tests = ["%s.%s" % (module_name, test_class_name)]
        sys.argv = ['', 'test'] + tests
        if verbose:
            sys.argv += ['-v2']
        else:
            sys.argv += ['-v0']
        if fail_fast:
            sys.argv += ['--failfast']

        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    def get_credentials(self):
        return self.create_basic(username = self.username, password = self.password)

    def tastypie_client(self, client_method, data = {}, authenticated = False):
        if authenticated:
            http_response = client_method(
                self.PATH, data = data, format = 'json', authentication=self.get_credentials()
            )
        else:
            http_response = client_method(
                self.PATH, data = data, format = 'json'
            )
#         if authenticated:
#             self.client.logout()

#         if http_response.content is '':
#             return {}, http_response.status_code
#         try:
#             response_json = json.loads(http_response.content)
#         except ValueError:
#             raise Exception("INVALID JSON: %r" % http_response.content)
#         return response_json, http_response.status_code
        return http_response

    def api_get(self, data = {}, authenticated = False):
        callback = self.tastypie_client(
            self.api_client.get,
            data = data,
            authenticated = authenticated
        )
        return callback

    def api_post(self, data = {}, authenticated = False):
        data = json.dumps(data)
        callback = self.tastypie_client(
            self.api_client.post,
            data = data,
            authenticated = authenticated
        )
        return callback