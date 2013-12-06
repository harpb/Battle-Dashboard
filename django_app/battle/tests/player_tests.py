from utilities.harp_test_case import HarpTestCase
from battle.models import Player

class TestPlayer(HarpTestCase):

    def setUp(self):
        self.player = Player.objects.get(id = 1)

    #===========================================================================
    # on_win
    #===========================================================================
    def test_on_win(self):
        # SETUP
        self.player.current_win_streak = 10
        expected_win_streak = 11
        expected_wins = 3
        # PRE-ASSERT
        self.assertEqual(expected_wins - 1, self.player.wins)
        # CALL
        self.player.on_win()
        # ASSERT
        self.assertEqual(expected_win_streak, self.player.current_win_streak)
        self.assertEqual(expected_wins, self.player.wins)

    def test_on_win_during_losing_streak(self):
        # SETUP
        self.player.current_win_streak = -10
        expected_win_streak = 1
        expected_wins = 3
        # PRE-ASSERT
        self.assertEqual(expected_wins - 1, self.player.wins)
        # CALL
        self.player.on_win()
        # ASSERT
        self.assertEqual(expected_win_streak, self.player.current_win_streak)
        self.assertEqual(expected_wins, self.player.wins)

    #===========================================================================
    # on_loss
    #===========================================================================
    def test_on_loss(self):
        # SETUP
        self.player.current_win_streak = -10
        expected_win_streak = -11
        expected_losses = 4
        # PRE-ASSERT
        self.assertEqual(expected_losses - 1, self.player.losses)
        # CALL
        self.player.on_loss()
        # ASSERT
        self.assertEqual(expected_win_streak, self.player.current_win_streak)
        self.assertEqual(expected_losses, self.player.losses)

    def test_on_loss_during_winning_streak(self):
        # SETUP
        self.player.current_win_streak = 10
        expected_win_streak = -1
        expected_losses = 4
        # PRE-ASSERT
        self.assertEqual(expected_losses - 1, self.player.losses)
        # CALL
        self.player.on_loss()
        # ASSERT
        self.assertEqual(expected_win_streak, self.player.current_win_streak)
        self.assertEqual(expected_losses, self.player.losses)


if __name__ == "__main__":
    test_methods = []
#     test_methods = ['test_on_win']
    module_name = 'battle.tests.player_tests'
    HarpTestCase.run_tests(
            module_name,
            'TestPlayer', test_methods,
            verbose = False, fail_fast = True
        )
