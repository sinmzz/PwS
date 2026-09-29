
from datetime import timedelta

from django.utils import timezone

from .models import Meeting, TimeSlot


def get_upcoming_meeting():
    today = timezone.localdate()
    days_until_saturday = (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_until_saturday)

    meeting, _ = Meeting.objects.get_or_create(
        saturday=saturday,
        defaults={"title": "Weekend Meeting"},
    )

    slots = [
        (TimeSlot.Day.SATURDAY, TimeSlot.Period.AFTERNOON),
        (TimeSlot.Day.SATURDAY, TimeSlot.Period.EVENING),
        (TimeSlot.Day.SATURDAY, TimeSlot.Period.LATE),
        (TimeSlot.Day.SUNDAY, TimeSlot.Period.AFTERNOON),
        (TimeSlot.Day.SUNDAY, TimeSlot.Period.EVENING),
        (TimeSlot.Day.SUNDAY, TimeSlot.Period.LATE),
    ]

    for day, period in slots:
        TimeSlot.objects.get_or_create(
            meeting=meeting,
            day=day,
            period=period,
        )

    return meeting