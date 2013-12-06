from utilities.harp_test_case import HarpTestCase
from battle.forms import PlayerForm
from battle.models import Player

class TestPlayerForm(HarpTestCase):

    def setUp(self):
        self.player_form = PlayerForm()

    #===========================================================================
    # is_valid
    #===========================================================================
    def test_is_valid(self):
        # SETUP
        expected = True
        data = {
            'nickname': 'leopard'
        }
        # CALL
        actual = PlayerForm(data = data).is_valid()
        # ASSERT
        self.assertEqual(expected, actual)

    def test_nickname_missing(self):
        # SETUP
        expected = False
        expected_error_count = 1
        expected_error_message = [u'This field is required.']
        data = {
            'nickname': None
        }
        form = PlayerForm(data = data)
        # CALL
        actual = form.is_valid()
        # ASSERT
        self.assertEqual(expected, actual)
        self.assertEqual(expected_error_count, len(form._errors))
        self.assertEqual(expected_error_message, form._errors['nickname'])

    def test_nickname_in_use(self):
        # SETUP
        expected = False
        expected_error_count = 1
        expected_error_message = [u'This nickname is already taken. Please choose another.']
        data = {
            'nickname': 'harp'
        }
        form = PlayerForm(data = data)
        # CALL
        actual = form.is_valid()
        # ASSERT
        self.assertEqual(expected, actual)
        self.assertEqual(expected_error_count, len(form._errors))
        self.assertEqual(expected_error_message, form._errors['nickname'])

    #===========================================================================
    # save
    #===========================================================================
    def test_save(self):
        # SETUP
        expected_id = 4
        data = {
            'nickname': 'leopard'
        }
        # CALL
        actual = PlayerForm(data = data).save()
        # ASSERT
        self.assertEqual(expected_id, actual.id)

    def test_patch_nickname(self):
        # SETUP
        expected_id = 1
        data = {
            'nickname': 'harpsie'
        }
        player = Player.objects.get(id = expected_id)
        # PRE CALL ASSERT
        self.assertNotEqual(player.nickname, data['nickname'])
        # CALL
        actual = PlayerForm(data = data, instance = player).save()
        # ASSERT
        self.assertEqual(expected_id, actual.id)
        self.assertEqual(player, actual)
        self.assertEqual(player.nickname, data['nickname'])

if __name__ == "__main__":
    test_methods = []
#     test_methods = ['test_is_valid']
    module_name = 'battle.tests.player_form_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestPlayerForm', test_methods,
            verbose = False, fail_fast = True
        )
