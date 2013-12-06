from django.db.models.signals import post_save
from django.dispatch import receiver
from battle.models import Battle

@receiver(post_save, sender = Battle)
def battle_saved(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.attacker == instance.winner:
        instance.attacker.on_win()
        instance.defender.on_loss()
    else:
        instance.attacker.on_loss()
        instance.defender.on_win()

    # Last seen is set to the latest battle
    # a player participates in
    if instance.attacker.last_seen < instance.end:
        instance.attacker.last_seen = instance.end
    if instance.defender.last_seen < instance.end:
        instance.defender.last_seen = instance.end

    # Save Changes
    instance.attacker.save()
    instance.defender.save()
