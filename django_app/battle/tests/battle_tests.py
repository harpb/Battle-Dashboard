from utilities.harp_test_case import HarpTestCase
from django.utils import timezone
from battle.models import Battle, Player

class TestBattle(HarpTestCase):

    def setUp(self):
        self.battle = Battle.objects.get(id = 1)

    #===========================================================================
    # on_save
    #===========================================================================
    def test_save(self):
        # SETUP
        attacker = Player.objects.get(id = 1)
        defender = Player.objects.get(id = 2)
        battle = Battle(
            attacker = attacker,
            defender = defender,
            winner = defender,
            start = timezone.now(),
            end = timezone.now()
        )
        # CALL
        battle.save()
        # ASSERT
        self.assertEqual(5, battle.id)

if __name__ == "__main__":
    test_methods = []
    test_methods = ['test_on_win']
    module_name = 'battle.tests.battle_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestBattle', test_methods,
            verbose = False, fail_fast = True
        )
