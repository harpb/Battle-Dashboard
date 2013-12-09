from utilities.harp_test_case import HarpTestCase
from mock import Mock

class TestPlayerResource(HarpTestCase):

    def setUp(self):
        super(TestPlayerResource, self).setUp()
        self.PATH = self.PATHS['player']

    #===========================================================================
    # get_list
    #===========================================================================
    def test_get_list_json(self):
        resp = self.api_get(authenticated = True)
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 3)

    #===========================================================================
    # post
    #===========================================================================
    def test_post_valid(self):
        # SETUP
        data = {
            'nickname': 'harmony'
        }
        # CALL
        resp = self.api_post(data = data, authenticated = True)
        # ASSERT
#         print resp.content
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    def test_post_missing_nickname(self):
        # SETUP
        data = {
            'nickname': ''
        }
        # CALL
        resp = self.api_post(data = data, authenticated = True)
        # ASSERT
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    def test_post_nickname_taken(self):
        # SETUP
        data = {
            'nickname': 'harp'
        }
        # CALL
        resp = self.api_post(data = data, authenticated = True)
        # ASSERT
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    #===========================================================================
    # update_nickname
    #===========================================================================
    def test_update_nickname(self):
        # SETUP
        data = {
            'nickname': 'harpsie'
        }
        # CALL
        resp = self.api_patch(oid = 2, data = data, authenticated = True)
        # ASSERT
#         print resp.content
        self.assertHttpAccepted(resp)
        self.assertValidJSON(resp.content)

    def test_update_nickname_fail(self):
        # SETUP
        data = {
            'nickname': 'harp'
        }
        # CALL
        resp = self.api_patch(oid = 2, data = data, authenticated = True)
        # ASSERT
#         print resp.content
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)


if __name__ == "__main__":
    test_methods = []
    test_methods = ['test_update_nickname_fail']
    module_name = 'battle.api.tests.player_resource_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestPlayerResource', test_methods,
            verbose = False, fail_fast = True
        )
