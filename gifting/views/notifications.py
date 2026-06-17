from django.shortcuts import get_object_or_404, render, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# from .mixins import HTMXMixin, WishDashContextMixin
from ..models import Notification


def unread_count(request):
    count = Notification.objects.filter(
        recipient=request.user,
        read_at__isnull=True
    ).count()
    return HttpResponse(count)


class NotificationListView(LoginRequiredMixin, generic.ListView):
    model = Notification
    template_name = "gifting/partials/notifications/_list.html"

    context_object_name = "notification_list"

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related("actor")


class NotificationReadView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        n = get_object_or_404(Notification, pk=pk, recipient=request.user)
        n.mark_read()
        return render(
            request, "gifting/partials/notifications/_item.html",
            {"n": n}
        )
