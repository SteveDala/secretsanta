from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import HTMXMixin, WishDashContextMixin
from ..models import WishList


class UserWishLists(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.ListView
):
    context_object_name = "user_wishlists"

    sidebar_template = "gifting/partials/wishlists/_sidebar.html"
    content_template = "gifting/partials/wishlists/_empty.html"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return self.request.user.wishlists.all()

    def render_to_response(self, context, **kwargs):
        if self.is_htmx:
            # HTMX only needs the content fragment
            return render(self.request, self.content_template, context)

        # Full dashboard render
        # context is a dict
        # **context expands it into keyword arguments
        dashboard_context = self.get_dashboard_context(**context)
        return self.render_dashboard(dashboard_context)


class WishListCreateView(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.CreateView
):
    model = WishList
    fields = ["name"]

    content_template = "gifting/partials/wishlists/_create.html"
    sidebar_template = "gifting/partials/wishlists/_sidebar.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({
            "placeholder": "Enter wishlist name..."
        })
        return form

    def render_to_response(self, context, **kwargs):
        if self.is_htmx:
            return render(self.request, self.content_template, context)
        dashboard_context = self.get_dashboard_context(**context)
        return self.render_dashboard(dashboard_context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if self.is_htmx:
            return render(
                self.request,
                "gifting/partials/wishlists/_wishlists_changed.html",
                {
                    "object": self.object,
                    "user_wishlists": self.request.user.wishlists.all(),
                    "content_template": "gifting/partials/wishlists/_detail.html",
                }
            )
        return super().form_valid(form)


class WishListEmptyView(LoginRequiredMixin, generic.TemplateView):
    template_name = "gifting/partials/wishlists/_empty.html"


class WishListDetailView(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.DetailView
):
    model = WishList
    sidebar_template = "gifting/partials/wishlists/_sidebar.html"
    content_template = "gifting/partials/wishlists/_detail.html"

    def get_queryset(self):
        return self.request.user.wishlists.all()

    def render_to_response(self, context, **kwargs):
        if self.is_htmx:
            return render(
                self.request,
                self.content_template,
                context
            )

        dashboard_context = self.get_dashboard_context(**context)
        return self.render_dashboard(dashboard_context)


class WishListDeleteView(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.DeleteView
):
    model = WishList

    sidebar_template = "gifting/partials/wishlists/_sidebar.html"
    content_template = "gifting/partials/wishlists/_empty.html"

    def get_queryset(self):
        return self.request.user.wishlists.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if self.is_htmx:
            return render(
                request,
                "gifting/partials/wishlists/_wishlists_changed.html",
                {
                    "user_wishlists": self.request.user.wishlists.all(),
                    "content_template": self.content_template,
                }
            )

        dashboard_context = self.get_dashboard_context(
            user_wishlists=request.user.wishlists.all()
        )
        return self.render_dashboard(dashboard_context)
