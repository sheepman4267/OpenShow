from slides.models import Deck, Theme, Display, Show
from django.views.generic import ListView

class IndexView(ListView):
    queryset = Show.objects.all()
    template_name = 'editor/index.html'
    extra_context = {
        'deck_list': Deck.objects.all,
        'theme_list': Theme.objects.all,
        'display_list': Display.objects.all,
    }


# TODO: Remove this entire view; it is probably not used anymore