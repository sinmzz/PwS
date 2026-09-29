
from django.conf import settings
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=200, default="Weekend Meeting")
    saturday = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-saturday"]

    def __str__(self):
        return f"{self.title} — {self.saturday}"


class TimeSlot(models.Model):
    class Day(models.TextChoices):
        SATURDAY = "sat", "Saturday"
        SUNDAY = "sun", "Sunday"

    class Period(models.TextChoices):
        AFTERNOON = "14", "2–4 pm"
        EVENING = "16", "4–6 pm"
        LATE = "18", "6–8 pm"

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="slots",
    )
    day = models.CharField(max_length=3, choices=Day.choices)
    period = models.CharField(max_length=2, choices=Period.choices)

    class Meta:
        ordering = ["day", "period"]
        constraints = [
            models.UniqueConstraint(
                fields=["meeting", "day", "period"],
                name="unique_meeting_slot",
            )
        ]

    def __str__(self):
        return f"{self.get_day_display()} {self.get_period_display()}"


class Vote(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meeting_votes",
    )
    slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["meeting", "user"],
                name="one_vote_per_meeting",
            )
        ]

    def __str__(self):
        return f"{self.user} — {self.slot}"