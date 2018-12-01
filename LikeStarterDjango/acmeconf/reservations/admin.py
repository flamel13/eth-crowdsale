from django.contrib import admin

from .models import Event
from .models import EventReservation
from .models import Document, Like, Wallet, ArtistContracts


admin.site.register(Event)
admin.site.register(EventReservation)
admin.site.register(Document)
admin.site.register(Like)
admin.site.register(Wallet)
admin.site.register(ArtistContracts)
