from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import WishList, Wish


class HTMXMixin:
    """
    This mixin allows each view to support two rendering modes:

    1. HTMX requests return partial HTML fragments (no layout)
    2. Normal requests render the full page (index.html)

    This enables progressive enhancement:
    - HTMX provides SPA-like interactivity
    - Normal requests still work (e.g. page reloads, direct URLs)
    """

    # Each view sets this to indicate which partial represents its UI state.
    # This avoids duplicating render logic across views.
    partial_template_name = None

    def render_to_response(self, context, **kwargs):
        """
        HTMX requests expect HTML fragments, not full pages. If we return
        the full template, HTMX will inject it into the page and we'll end
        up with a "page inside a page."
        """
        if self.request.headers.get("HX-Request"):
            if self.partial_template_name:
                return render(
                    self.request,
                    self.partial_template_name,
                    context
                )

            # Some views (like Dashboard) don't have a main content partial.
            # For HTMX requests, we return an "empty" fragment to clear panel.
            return render(
                self.request,
                "gifting/partials/_empty.html",
                context
            )

        # The sidebar depends on user_wishlists, so we always include it
        # during full-page renders to keep the layout consistent.
        context["user_wishlists"] = self.request.user.wishlists.all()

        # index.html uses selected_partial to decide what to render in the
        # main content area. Without this, it falls back to a default state.
        if self.partial_template_name:
            context["selected_partial"] = self.partial_template_name

        # We override Django's default rendering flow because it assumes
        # full-page responses. HTMX requires partial responses instead.
        return render(
            self.request,
            "gifting/index.html",
            context
        )

    def render_main_sections(self, *, wishlist=None, selected_partial=None):
        """
        """
        return render(
            self.request,
            "gifting/partials/_main_app_sections.html",
            {
                "object": wishlist,
                "user_wishlists": self.request.user.wishlists.all(),
                "selected_partial": selected_partial,
            }
        )


class DashboardView(LoginRequiredMixin, HTMXMixin, generic.ListView):
    template_name = "gifting/index.html"
    context_object_name = "user_wishlists"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return self.request.user.wishlists.all().order_by("-created_at")


class WishListCreateView(LoginRequiredMixin, HTMXMixin, generic.CreateView):
    model = WishList
    fields = ["name"]
    partial_template_name = "gifting/partials/_new_wishlist.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({
            "placeholder": "Enter wishlist name..."
        })
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            return self.render_main_sections(
                wishlist=self.object,
                selected_partial="gifting/partials/_wishlist_detail.html"
            )
        return super().form_valid(form)


class WishListDetailView(LoginRequiredMixin, HTMXMixin, generic.DetailView):
    model = WishList
    partial_template_name = "gifting/partials/_wishlist_detail.html"

    def get_queryset(self):
        return self.request.user.wishlists.all()


class WishListDeleteView(LoginRequiredMixin, HTMXMixin, generic.DeleteView):
    model = WishList

    def get_queryset(self):
        return self.request.user.wishlists.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if request.headers.get("HX-Request"):
            return self.render_main_sections(
                selected_partial=None,
            )

        return redirect("gifting:dashboard")


class WishCreateView(LoginRequiredMixin, HTMXMixin, generic.CreateView):
    model = Wish
    fields = ["title", "description", "price", "url"]
    partial_template_name = "gifting/partials/_wish_form.html"

    def get_wishlist(self):
        return WishList.objects.get(
            pk=self.kwargs["wishlist_id"],
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlist"] = self.get_wishlist()
        return context

    def form_valid(self, form):
        wishlist = self.get_wishlist()

        form.instance.wishlist = wishlist
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            return self.render_main_sections(
                wishlist=wishlist,
                selected_partial="gifting/partials/_wishlist_detail.html"
            )
        return super().form_valid(form)


class WishUpdateView(LoginRequiredMixin, HTMXMixin, generic.UpdateView):
    model = Wish
    fields = ["title", "description", "price", "url"]
    partial_template_name = "gifting/partials/_wish_form.html"

    def get_queryset(self):
        return Wish.objects.filter(wishlist__user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get("HX-Request"):
            return self.render_main_sections(
                wishlist=self.object.wishlist,
                selected_partial="gifting/partials/_wishlist_detail.html"
            )

        return redirect("gifting:detail", pk=self.object.wishist.id)


class WishDeleteView(LoginRequiredMixin, HTMXMixin, generic.DeleteView):
    model = Wish

    def get_queryset(self):
        return Wish.objects.filter(wishlist__user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        wishlist = self.object.wishlist

        self.object.delete()

        if request.headers.get("HX-Request"):
            return self.render_main_sections(
                wishlist=wishlist,
                selected_partial="gifting/partials/_wishlist_detail.html"
            )
        return redirect("gifting:detail", pk=wishlist.id)
