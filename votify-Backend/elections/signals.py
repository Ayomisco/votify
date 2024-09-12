from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vote, Candidate
from results.models import Result
# Signal to update the vote count when a vote is cast


@receiver(post_save, sender=Vote)
def update_vote_count_on_save(sender, instance, **kwargs):
    candidate = instance.candidate
    candidate.votes_count = Vote.objects.filter(candidate=candidate).count()
    candidate.save()

# Signal to update the vote count when a vote is removed


@receiver(post_delete, sender=Vote)
def update_vote_count_on_delete(sender, instance, **kwargs):
    candidate = instance.candidate
    candidate.votes_count = Vote.objects.filter(candidate=candidate).count()
    candidate.save()
# Signal to update the result after a vote is saved


@receiver(post_save, sender=Vote)
def update_result_after_vote(sender, instance, **kwargs):
    # Recalculate the votes for the election and candidates
    result, created = Result.objects.get_or_create(election=instance.election)
    result.calculate_results()
    result.calculate_total_votes()
