from utilities.harp_test_case import HarpTestCase
from battle.forms import BattleForm, PlayerForm
from battle.models import Battle, Player
from django.utils import timezone

class TestBattleForm(HarpTestCase):

    def setUp(self):
        self.battle_form = BattleForm()

    #===========================================================================
    # is_valid
    #===========================================================================
    def test_is_valid(self):
        # SETUP
        expected = True
        data = {
            'attacker': 1,
            'defender': 2,
            'winner': 1,
            'start': timezone.now(),
            'end': timezone.now()
        }
        form = BattleForm(data = data)
        # CALL
        actual = form.is_valid()
        # ASSERT
        print form._errors
        self.assertEqual(expected, actual)

    def test_fields_missing(self):
        # SETUP
        expected = False
        expected_error_count = 5
        expected_error_message = [u'This field is required.']
        data = {}
        form = BattleForm(data = data)
        # CALL
        actual = form.is_valid()
        # ASSERT
#         print form._errors
        self.assertEqual(expected, actual)
        self.assertEqual(expected_error_count, len(form._errors))
        for field_key, field_error in form._errors.iteritems():
            self.assertEqual(expected_error_message, field_error)

    def test_not_actual_player_and_ends_too_early(self):
        # SETUP
        expected = False
        expected_error_count = 4
        player_does_not_exist = [u'Select a valid choice. That choice is not one of the available choices.']
        data = {
            'attacker': 11,
            'defender': 12,
            'winner': 1,
            'start': '2006-10-25 14:30:40',
            'end': '2006-10-25 14:30:20'
        }
        form = BattleForm(data = data)
        # CALL
        actual = form.is_valid()
        # ASSERT
#         print form._errors
        self.assertEqual(expected, actual)
        self.assertEqual(expected_error_count, len(form._errors))
        self.assertEqual(player_does_not_exist, form._errors['attacker'])
        self.assertEqual(player_does_not_exist, form._errors['defender'])
        self.assertEqual([BattleForm.PLAYERS_ERROR], form._errors['winner'])
        self.assertEqual([BattleForm.END_IS_BEFORE_START], form._errors['end'])

    def test_winner_not_a_player(self):
        # SETUP
        expected = False
        expected_error_count = 1
        data = {
            'attacker': 1,
            'defender': 2,
            'winner': 3,
            'start': '2006-10-25 14:30:40',
            'end': '2006-10-25 14:30:40'
        }
        form = BattleForm(data = data)
        # CALL
        actual = form.is_valid()
        # ASSERT
#         print form._errors
        self.assertEqual(expected, actual)
        self.assertEqual(expected_error_count, len(form._errors))
        self.assertEqual([BattleForm.WINNER_NOT_A_PLAYER], form._errors['winner'])

    #===========================================================================
    # save
    #===========================================================================
    def test_save(self):
        # SETUP
        expected_id = 5
        data = {
            'attacker': 1,
            'defender': 2,
            'winner': 1,
            'start': timezone.now(),
            'end': timezone.now()
        }
        # CALL
        actual = BattleForm(data = data).save()
        # ASSERT
        self.assertEqual(expected_id, actual.id)


if __name__ == "__main__":
    test_methods = []
#     test_methods = ['test_is_valid']
    module_name = 'battle.tests.battle_form_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestBattleForm', test_methods,
            verbose = False, fail_fast = True
        )
