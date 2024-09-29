from .models import Candidate, Election
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from .models import Election, Candidate, Vote
from django.db.models import Count
from django.db import transaction
from django.db.models import F


def election_list(request):
    """
    View to display the list of elections.
    Filters elections based on the election_type if provided.
    Categorizes elections into active, upcoming, and finished.
    """
    now = timezone.now()

    # Get the election type filter from the GET parameters
    ELECTION_TYPE_CHOICES_filter = request.GET.get('election_type')

    # Filter elections based on the provided election type or get all elections
    if ELECTION_TYPE_CHOICES_filter:
        elections = Election.objects.filter(
            election_type=ELECTION_TYPE_CHOICES_filter)
    else:
        elections = Election.objects.all()

    # Categorize elections based on the current date
    active_elections = elections.filter(start_date__lte=now, end_date__gte=now)
    upcoming_elections = elections.filter(start_date__gt=now)
    finished_elections = elections.filter(end_date__lt=now)

    # Get a dictionary of election types for display purposes
    election_types = dict(Election.ELECTION_TYPE_CHOICES)

    # Context to pass to the template
    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'finished_elections': finished_elections,
        'election_types': election_types,
    }

    return render(request, 'elections.html', context)


def voting_page(request, election_id):
    """
    View to display the voting page for a specific election.
    Checks if the election is currently active; otherwise, redirects with an error.
    """
    # Retrieve the election object or return a 404 error if not found
    election = get_object_or_404(Election, id=election_id)
    now = timezone.now()

    # Check if the election is within the active period
    if election.start_date > now or election.end_date < now:
        messages.error(request, "This election is not currently active.")
        return redirect('election_list')

    return render(request, 'voting.html', {'election': election})


def vote(request, election_id, candidate_id):
    """
    View to handle voting for a candidate in a specific election.
    Ensures atomic transaction to avoid race conditions.
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election = get_object_or_404(Election, id=election_id)

    if request.method == "POST":
        if election.start_date <= timezone.now() <= election.end_date:
            with transaction.atomic():
                vote, created = Vote.objects.get_or_create(
                    user=request.user,
                    election=election,
                    defaults={'candidate': candidate}
                )
                if created:
                    # Use F-expression to prevent race conditions
                    candidate.votes_count = F('votes_count') + 1
                    candidate.save(update_fields=['votes_count'])
                    messages.success(
                        request, "Your vote has been successfully recorded."
                    )
                else:
                    messages.error(
                        request, "You have already voted in this election."
                    )
        else:
            messages.error(
                request, "Voting is not allowed outside of the election period."
            )

    return redirect('voting_page', election_id=election.id)


def manifesto_view(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    return JsonResponse({
        'full_name': candidate.full_name,
        'manifesto': candidate.manifesto,
    })


# elections/views.py


def candidates_list(request):
    election_type = request.GET.get('election_type', None)
    print(f"Election type: {election_type}")  # Debug line

    if election_type:
        candidates = Candidate.objects.filter(
            election__election_type=election_type)
    else:
        candidates = Candidate.objects.all()

    # Order candidates by votes_count
    candidates = candidates.order_by('-votes_count')

    data = []
    for candidate in candidates:
        data.append({
            'full_name': candidate.full_name,
            'department': candidate.department,
            'votes_count': candidate.votes_count,
            'position': get_candidate_position(candidate),
        })

    return JsonResponse({'candidates': data})



def get_candidate_position(candidate):
    all_candidates = Candidate.objects.filter(
        election=candidate.election).order_by('-votes_count')

    # Check the position within the ordered list
    position = list(all_candidates).index(candidate) + 1

    # Assign position based on rank
    if candidate.votes_count == 0:
        return 'No Votes Yet'
    elif position == 1:
        return 'Winner'
    elif position == 2:
        return 'Runner-up'
    elif position == 3:
        return 'Second Runner-up'
    else:
        return f'{position}th Place'



def candidates_page(request):
    # Get the current date and time
    current_time = timezone.now()

    # Filter for active elections
    elections = Election.objects.filter(
        start_date__lte=current_time, end_date__gte=current_time)

    return render(request, 'candidates_page.html', {'elections': elections})
