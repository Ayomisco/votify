from django.db import models
from django.utils import timezone
from elections.models import Election, Candidate, Vote


class Result(models.Model):
    election = models.OneToOneField(
        Election, on_delete=models.CASCADE, related_name='result')
    total_votes = models.PositiveIntegerField(default=0)
    announced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Result for {self.election}"

    def calculate_total_votes(self):
        self.total_votes = Vote.objects.filter(election=self.election).count()
        self.save()


    def calculate_results(self):
        candidates = Candidate.objects.filter(election=self.election)
        for candidate in candidates:
            vote_count = Vote.objects.filter(
                candidate=candidate, election=self.election
            ).count()
            candidate.votes_count = vote_count
            candidate.save()

        self.calculate_total_votes()

        # Automatically create Winner entries
        winners = self.get_winner()
        # Remove old winners if any
        Winner.objects.filter(result=self).delete()
        for winner in winners:
            Winner.objects.create(result=self, candidate=winner)
            
    def get_winner(self):
        candidates = Candidate.objects.filter(election=self.election)
        if not candidates:
            return []
        max_votes = max(
            candidates, key=lambda candidate: candidate.votes_count)
        winners = [
            candidate for candidate in candidates if candidate.votes_count == max_votes.votes_count]
        return winners

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'



class Winner(models.Model):
    result = models.ForeignKey(
        Result, on_delete=models.CASCADE, related_name='winners'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='winners'
    )  # Changed related_name to 'winners' for clarity
    announced_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Winner: {self.candidate.full_name} in {self.result.election}"

    class Meta:
        verbose_name = 'Winner'
        verbose_name_plural = 'Winners'
