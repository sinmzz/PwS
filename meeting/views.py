from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Vote
from .services import get_upcoming_meeting


@login_required
def index(request):
    meeting = get_upcoming_meeting()

    current_vote = Vote.objects.filter(
        meeting=meeting,
        user=request.user,
    ).first()

    return render(request, "meeting/index.html", {
    	"meeting": meeting,
    	"current_vote": current_vote,
    	"sunday": meeting.saturday + timedelta(days=1),
	})


@login_required
@require_POST
def vote(request):
    meeting = get_upcoming_meeting()

    slot = get_object_or_404(
        meeting.slots,
        pk=request.POST.get("slot"),
    )

    Vote.objects.update_or_create(
        meeting=meeting,
        user=request.user,
        defaults={"slot": slot},
    )

    return redirect("meeting:index")