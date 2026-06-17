from django.shortcuts import render
from ..models import Event


class HTMXMixin:
    """
    This mixin injects the `is_htmx` function to each view
    that inherits it.

    Remember:
    1. HTMX requests return partial HTML fragments (no layout)
    2. Normal requests render the full page (dashboard.html)

    """
    @property
    def is_htmx(self):
        return self.request.headers.get("HX-Request")


class WishDashContextMixin:
    sidebar_template = None
    content_template = None

    def get_dashboard_context(self, **kwargs):
        return {
            "user_wishlists": self.request.user.wishlists.all(),
            "sidebar_template": self.sidebar_template,
            "content_template": self.content_template,
            **kwargs,
        }

    def render_dashboard(self, context):
        return render(self.request, "gifting/partials/wishlists/_dashboard.html", context)


class EventDashContextMixin:
    sidebar_template = None
    main_panel_template = None
    secondary_panel_template = None

    def get_eventsdash_context(self, **kwargs):
        return {
            "user_events": (
                Event.objects
                .filter(participants__user=self.request.user)
                .distinct()
            ),
            "sidebar_template": self.sidebar_template,
            "main_panel_template": self.main_panel_template,
            "secondary_panel_template": self.secondary_panel_template,
            ** kwargs,
        }

    def render_eventsdash(self, context):
        return render(self.request, "gifting/partials/events/_dashboard.html", context)
