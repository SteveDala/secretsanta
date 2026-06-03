from django.shortcuts import render


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
