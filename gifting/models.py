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
    class EventType(models.TextChoices):
        SECRET_SANTA = "secret_santa"
        BIRTHDAY = "birthday"
        GENERAL = "general"

    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
    )
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_associations"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participants"
    )

    def clean(self):
        if self.wishlist is not None:
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


class Matchup(models.Model):
    giver = models.OneToOneField(
        EventParticipant,
        related_name="assignment",
        on_delete=models.CASCADE,
    )

    receiver = models.ForeignKey(
        EventParticipant,
        related_name="giver",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.giver.event != self.receiver.event:
            raise ValidationError(
                "Matchup participants must belong to the same event."
            )

        if self.giver == self.receiver:
            raise ValidationError(
                "Participants cannot match with themselves."
            )
