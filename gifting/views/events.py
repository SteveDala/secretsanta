from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import HTMXMixin, EventDashContextMixin
from ..models import Event, EventParticipant, WishList


class EventsList(
    LoginRequiredMixin,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        participant = self.object.participants.get(
            user=self.request.user
        )

        context["participant"] = participant

        context["available_wishlists"] = (
            self.request.user.wishlists.all()
        )

        return context

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


class EventEmpty(
    LoginRequiredMixin,
    HTMXMixin,
    EventDashContextMixin,
    generic.View,
):
    main_panel_template = "gifting/partials/events/_empty.html"
    secondary_panel_template = "gifting/partials/events/_empty.html"

    def get(self, request):
        context = self.get_eventsdash_context()

        if self.is_htmx:
            return render(
                request,
                "gifting/partials/events/_close_event_htmx.html",
                context,
            )


class EventParticipantSetWishList(
    LoginRequiredMixin,
    HTMXMixin,
    EventDashContextMixin,
    generic.View
):
    sidebar_template = "gifting/partials/events/_sidebar.html"
    main_panel_template = "gifting/partials/events/_event_header.html"
    secondary_panel_template = "gifting/partials/events/_event_participants.html"

    def post(self, request, pk):
        event = get_object_or_404(
            Event,
            participants__user=request.user,
            pk=pk
        )

        participant = get_object_or_404(
            EventParticipant,
            event=event,
            user=request.user
        )

        if request.POST["wishlist_id"] != "null":
            wishlist = get_object_or_404(
                WishList,
                pk=request.POST["wishlist_id"],
                user=request.user
            )
        else:
            wishlist = None

        participant.wishlist = wishlist
        participant.save()

        context = self.get_eventsdash_context(
            object=event,
            event=event,
            participant=participant,
            available_wishlists=request.user.wishlists.all()
        )

        if self.is_htmx:
            return render(
                request,
                "gifting/partials/events/_event_header.html",
                context
            )
        else:
            redirect('gifting:event_detail', kwargs={'pk': event.pk})

    def get(self, request, pk):
        event = get_object_or_404(
            Event,
            participants__user=request.user,
            pk=pk
        )
        return redirect('gifting:event_detail', pk=event.pk)
