from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "gifting/dashboard.html"

    sidebar_template = "gifting/partials/home/_sidebar.html"
    content_template = "gifting/partials/home/_news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["sidebar_template"] = self.sidebar_template
        context["content_template"] = self.content_template
        context["user_wishlists"] = self.request.user.wishlists.all()

        return context
