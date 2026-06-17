from django.contrib import admin
from .models import WishList, Wish, Event, EventParticipant, Notification

# Register your models here.

admin.site.register(WishList)
admin.site.register(Wish)
admin.site.register(Event)
admin.site.register(EventParticipant)
admin.site.register(Notification)
