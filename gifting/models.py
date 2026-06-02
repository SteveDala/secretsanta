from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class WishList(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user})"


class Wish(models.Model):

    wishlist = models.ForeignKey(
        WishList,
        on_delete=models.CASCADE,
        related_name="wishes"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="administered_events"
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventParticipant(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_participations"
    )

    wishlist = models.ForeignKey(
        WishList,
        on_delete=models.CASCADE,
        related_name="event_associations"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participants"
    )

    def clean(self):
        if self.wishlist.user != self.user:
            raise ValidationError(
                "Participant must use their own wishlist."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "user"],
                name="unique_event_participant"
            ),
            models.UniqueConstraint(
                fields=["event", "wishlist"],
                name="unique_wishlist_per_event"
            )
        ]
