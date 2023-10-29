from django.views.generic.edit import FormView
from .forms import DeckFromImagesForm

from slides.models import Deck, Slide, SlideElement, Transition


class DeckFromImagesFormView(FormView):
    form_class = DeckFromImagesForm
    template_name = "deck_from_images/upload.html"
    # success_url = "..."  # Replace with your URL or reverse().

    def __init__(self):
        self.new_deck = None
        super().__init__()

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["files"]
        new_default_transition = Transition.objects.get(pk=form.cleaned_data["transition_pk"])
        self.new_deck = Deck(
            name=form.cleaned_data["name"],
            default_transition=new_default_transition,
        )
        self.new_deck.save()
        for image in files:
            print('image!')
            new_slide = Slide(deck=self.new_deck)
            new_slide.save()
            new_slide_element = SlideElement(
                css_class=form.cleaned_data["image_css_class"],
                order=0,
                slide=new_slide,
                image=image,
                body="",
            )
            new_slide_element.save()
        return super().form_valid(self)

    def get_success_url(self):
        return self.new_deck.get_absolute_url()
