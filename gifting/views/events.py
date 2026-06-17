from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import HTMXMixin, EventDashContextMixin
from ..models import Event, EventParticipant


class EventsList(
    LoginRequiredMixin,
    HTMXMixin,
    EventDashContextMixin,
    generic.ListView
):
    context_object_name = "user_events"

    sidebar_template = "gifting/partials/events/_sidebar.html"
    main_panel_template = "gifting/partials/events/_empty.html"
    secondary_panel_template = "gifting/partials/events/_empty.html"

    def get_queryset(self):
        return Event.objects.filter(
            participants__user=self.request.user
        )

    def render_to_response(self, context, **kwargs):

        dashboard_context = self.get_eventsdash_context(**context)

        if self.is_htmx:
            return render(self.request, self.content_template, context)

        return self.render_eventsdash(dashboard_context)


class EventDetail(
    LoginRequiredMixin,
    HTMXMixin,
    EventDashContextMixin,
    generic.DetailView
):
    model = Event
    sidebar_template = "gifting/partials/events/_sidebar.html"
    main_panel_template = "gifting/partials/events/_event_header.html"
    secondary_panel_template = "gifting/partials/events/_event_participants.html"

    def get_queryset(self):
        return Event.objects.filter(
            participants__user=self.request.user
        )

    def render_to_response(self, context, **kwargs):

        dashboard_context = self.get_eventsdash_context(**context)

        if self.is_htmx:
            return render(
                self.request,
                "gifting/partials/events/_event_detail_htmx.html",
                dashboard_context
            )

        return self.render_eventsdash(dashboard_context)
