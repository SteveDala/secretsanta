from django.db import models
from django.conf import settings


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
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
