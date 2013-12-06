from django.db import models
from model_utils.models import TimeStampedModel, TimeFramedModel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Player(TimeStampedModel):
    # Personal
    first_name = models.CharField(_('first name'), max_length = 30, blank = True)
    last_name = models.CharField(_('last name'), max_length = 30, blank = True)
    nickname = models.CharField(
        _('last name'), max_length = 30, blank = True, unique = True)
    # Stats
    current_win_streak = models.IntegerField(default = 0)
    losses = models.PositiveIntegerField(default = 0)
    wins = models.PositiveIntegerField(default = 0)
    # Status
    last_seen = models.DateTimeField(_('last seen'), default = timezone.now)

    def on_win(self, save = False):
        if self.current_win_streak < 0:
            self.current_win_streak = 0
        self.current_win_streak += 1
        self.wins += 1
        if save:
            self.save()

    def on_loss(self, save = False):
        if self.current_win_streak > 0:
            self.current_win_streak = 0
        self.current_win_streak += -1
        self.losses += 1
        if save:
            self.save()

class Battle(TimeFramedModel):
    attacker = models.ForeignKey(Player, related_name = 'attacker')
    defender = models.ForeignKey(Player, related_name = 'defender')
    winner = models.ForeignKey(Player, related_name = 'winner')
