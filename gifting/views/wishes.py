from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import HTMXMixin, WishDashContextMixin
from ..models import Wish, WishList


class WishCreateView(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.CreateView
):
    model = Wish
    fields = ["title", "description", "price", "url"]

    sidebar_template = "gifting/partials/wishlists/_sidebar.html"
    content_template = "gifting/partials/wishlists/_wish_form.html"

    def get_wishlist(self):
        return WishList.objects.get(
            pk=self.kwargs["wishlist_id"],
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlist"] = self.get_wishlist()
        return context

    def render_to_response(self, context, **kwargs):
        if self.is_htmx:
            return render(self.request, self.content_template, context)

        dashboard_context = self.get_dashboard_context(**context)
        return self.render_dashboard(dashboard_context)

    def form_valid(self, form):
        wishlist = self.get_wishlist()

        form.instance.wishlist = wishlist
        self.object = form.save()

        if self.is_htmx:
            return render(
                self.request,
                "gifting/partials/wishlists/_detail.html",
                {"object": wishlist}
            )
        return super().form_valid(form)


class WishUpdateView(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.UpdateView
):
    model = Wish
    fields = ["title", "description", "price", "url"]

    sidebar_template = "gifting/partials/wishlists/_sidebar.html"
    content_template = "gifting/partials/wishlists/_wish_form.html"

    def get_queryset(self):
        return Wish.objects.filter(wishlist__user=self.request.user)

    def render_to_response(self, context, **kwargs):
        if self.is_htmx:
            return render(self.request, self.content_template, context)

        dashboard_context = self.get_dashboard_context(**context)
        return self.render_dashboard(dashboard_context)

    def form_valid(self, form):
        self.object = form.save()

        if self.is_htmx:
            return render(
                self.request,
                "gifting/partials/wishlists/_detail.html",
                {"object": self.object.wishlist}
            )

        return redirect("gifting:detail", pk=self.object.wishlist.id)


class WishDeleteView(
    LoginRequiredMixin,
    HTMXMixin,
    WishDashContextMixin,
    generic.DeleteView
):
    model = Wish

    sidebar_template = "gifting/partials/wishlists/_sidebar.html"
    content_template = "gifting/partials/wishlists/_detail.html"

    def get_queryset(self):
        return Wish.objects.filter(wishlist__user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        wishlist = self.object.wishlist

        self.object.delete()

        if self.is_htmx:
            return render(
                self.request,
                self.content_template,
                {"object": wishlist}
            )

        dashboard_context = self.get_dashboard_context(object=wishlist)
        return self.render_dashboard(dashboard_context)
