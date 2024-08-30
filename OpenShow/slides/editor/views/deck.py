from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from slides.models import Deck, Slide
from django.db import transaction
from django.shortcuts import get_object_or_404, HttpResponseRedirect
import slides.aoml_parser as aoml


class DeckCreateView(CreateView):
    model = Deck
    template_name = 'editor/snippets/hx-simple_create_form.html'
    fields = ['name']
    extra_context = {
        'action': 'new-deck',
        'object_type': 'Deck',
    }


# class DeckUpdateView(UpdateView):
#     model = Deck
#     template_name = 'editor/edit_deck.html'
#     fields = ['name', 'theme']


class DeckEditorView(UpdateView):
    queryset = Deck.objects.all()
    model = Deck
    fields = [
        'name',
        'theme',
        'default_transition',
        'default_transition_duration',
        'default_auto_advance',
        'default_auto_advance_duration',
        'script',
        'slide_text_markup',
    ]
    template_name = 'editor/deck_editor.html'
    # extra_context = {'display': Display.objects.all().first()}


class DeckDeleteView(DeleteView):
    model = Deck
    success_url = reverse_lazy('slides-index')
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-deck',
    }


def push_deck_cues(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    deck.push_cues()
    return HttpResponseRedirect(deck.get_absolute_url())


@transaction.atomic()
def push_deck_slide_text(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    existing_slides = list(deck.slides.all())
    if len(existing_slides) > 0:
        for slide in existing_slides:  # TODO: Add some options here...
            slide.delete()
    for slide_markup in aoml.parse_markup(deck.slide_text_markup):
        slide = Slide(deck=deck)
        slide.save()
        for element in aoml.parse_slide(slide_markup):
            element.slide = slide
            element.save()
    return HttpResponseRedirect(deck.get_absolute_url())


def pull_aoml_text(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    deck.slide_text_markup = deck.pull_aoml()
    deck.save()
    return HttpResponseRedirect(deck.get_absolute_url())
