from django.contrib import admin
from .models import Meeting, TimeSlot, Vote


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 0


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "saturday")
    inlines = [TimeSlotInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "meeting", "slot", "created_at")
    list_filter = ("meeting", "slot")
    search_fields = ("user__username",)