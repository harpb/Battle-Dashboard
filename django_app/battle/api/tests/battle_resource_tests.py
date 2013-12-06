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


if __name__ == "__main__":
    test_methods = []
#     test_methods = ['test_get_list_json']
    module_name = 'battle.api.tests.battle_resource_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestBattleResource', test_methods,
            verbose = False, fail_fast = True
        )
