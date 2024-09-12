# results/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elections.models import Vote
from .models import Result


@receiver(post_save, sender=Vote)
def update_results_on_vote_save(sender, instance, **kwargs):
    election = instance.election
    try:
        result = election.result
    except Result.DoesNotExist:
        result = Result.objects.create(election=election)

    result.calculate_results()
    result.calculate_total_votes()


@receiver(post_delete, sender=Vote)
def update_results_on_vote_delete(sender, instance, **kwargs):
    election = instance.election
    try:
        result = election.result
    except Result.DoesNotExist:
        result = Result.objects.create(election=election)

    result.calculate_results()
    result.calculate_total_votes()
