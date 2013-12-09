from utilities.harp_test_case import HarpTestCase

class TestBattleResource(HarpTestCase):

    def setUp(self):
        super(TestBattleResource, self).setUp()
        self.PATH = self.PATHS['battle']

    #===========================================================================
    # Authorization Tests
    #===========================================================================
    def test_get_list_unauthorzied(self):
        # CALL
        resp = self.api_get()
        # ASSERT
        self.assertHttpUnauthorized(resp)

    def test_get_list_authorzied(self):
        # CALL
        resp = self.api_get(authenticated = True)
        # ASSERT
        self.assertHttpAuthorized(resp)

    def test_get_list_json(self):
        resp = self.api_get(authenticated = True)
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 4)

    #===========================================================================
    # post
    #===========================================================================
    def test_post_valid(self):
        # SETUP
        data = {
            'attacker': '1',
            'defender': '2',
            'winner': '2',
            'start': '2006-10-25 14:30:00',
            'end': '2006-10-25 14:30:20'
        }
        # CALL
        resp = self.api_post(data = data, authenticated = True)
        # ASSERT
#         print resp.content
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    def test_post_invalid_datetime(self):
        # SETUP
        data = {
            'attacker': '1',
            'defender': '2',
            'winner': '2',
            'start': '2013-12-05T23:48:59',
            'end': '2013-01-01 12:25 AM'
        }
        # CALL
        resp = self.api_post(data = data, authenticated = True)
        # ASSERT
        print resp.content
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    def test_post_missing_fields(self):
        # SETUP
        data = {
        }
        # CALL
        resp = self.api_post(data = data, authenticated = True)
        # ASSERT
        print resp.content
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

if __name__ == "__main__":
    test_methods = []
    test_methods = ['test_post_invalid_datetime']
    module_name = 'battle.api.tests.battle_resource_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestBattleResource', test_methods,
            verbose = False, fail_fast = True
        )
