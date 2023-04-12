from django.contrib import admin
from .models import Slide, SlideElement, Deck, Display, Segment, Show, Theme

# Register your models here.
admin.site.register(Slide)
admin.site.register(SlideElement)
admin.site.register(Deck)
admin.site.register(Display)
admin.site.register(Segment)
admin.site.register(Show)
admin.site.register(Theme)