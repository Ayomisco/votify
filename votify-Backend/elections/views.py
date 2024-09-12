from django.contrib import messages
from .models import Election, Candidate, Vote
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Election
from django.utils import timezone


def election_list(request):
    now = timezone.now()
    ELECTION_TYPE_CHOICES_filter = request.GET.get('election_type')

    # Filter elections by type if provided
    if ELECTION_TYPE_CHOICES_filter:
        elections = Election.objects.filter(
            election_type=ELECTION_TYPE_CHOICES_filter)
    else:
        elections = Election.objects.all()

    # Categorize elections
    active_elections = elections.filter(start_date__lte=now, end_date__gte=now)
    upcoming_elections = elections.filter(start_date__gt=now)
    finished_elections = elections.filter(end_date__lt=now)

    # Get distinct election types for filter options
    # Create a dict from choices
    election_types = dict(Election.ELECTION_TYPE_CHOICES)

    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'finished_elections': finished_elections,
        'election_types': election_types,  # Pass the dict to the context
    }

    return render(request, 'elections.html', context)


def voting_page(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    now = timezone.now()

    # Ensure that voting is happening during the election period
    if election.start_date > now or election.end_date < now:
        messages.error(request, "This election is not currently active.")
        return redirect('election_list')

    return render(request, 'voting.html', {'election': election})


def vote(request, election_id, candidate_id):
    # Fetch the candidate and associated election
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election = get_object_or_404(Election, id=election_id)

    if request.method == "POST":
        # Ensure that voting is happening during the election period
        if election.start_date <= timezone.now() <= election.end_date:
            # Check if the user has already voted in this election
            vote, created = Vote.objects.get_or_create(
                user=request.user,
                election=election,
                defaults={'candidate': candidate}
            )
            if created:
                # Increment vote count if new vote is created
                candidate.votes_count += 1
                candidate.save()
                messages.success(request, "Your vote has been recorded.")
            else:
                messages.error(
                    request, "You have already voted in this election.")
        else:
            messages.error(
                request, "Voting is not allowed outside of the election period.")

    # Redirect back to the voting page for the election
    return redirect('voting_page', election_id=election.id)
