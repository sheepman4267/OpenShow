from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from slides.models import Deck, Slide, SlideElement
from django.db import transaction
from django.shortcuts import get_object_or_404, HttpResponseRedirect
import slides.aoml_parser as aoml
from slides.editor.forms import DeckFromImagesForm, ImportImagesForm


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
        'advance_in_loop',
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


class DeckFromImagesView(FormView):
    form_class = DeckFromImagesForm
    template_name = 'editor/snippets/hx-simple_create_form.html'
    extra_context = {
        'previous_page': 'slides-index',
        'action': 'import-deck-from-images',
        'object_type': 'Deck From Many Images',
    }

    def form_valid(self, form):
        files = form.cleaned_data['files']
        print(files)
        print('^^FILES')
        form.save()
        for image in files:
            new_slide = Slide(deck=form.instance)
            new_slide.save()
            new_slide_element = SlideElement(
                css_class=form.cleaned_data["image_css_class"],
                order=0,
                slide=new_slide,
                image=image,
                body="",
            )
            new_slide_element.save()
        return HttpResponseRedirect(reverse_lazy('edit-deck', kwargs={'pk': form.instance.pk}))


class ImportImagesToExistingDeckView(FormView):
    model = Deck
    form_class = ImportImagesForm
    template_name = 'editor/import_images_to_deck.html'

    def get_object(self):
        db_object = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return db_object

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['deck'] = self.get_object()
        return context

    def form_valid(self, form):
        deck = self.get_object()
        # If we're in overwrite mode, delete all the deck's slides first
        if form.cleaned_data['mode'] == ImportImagesForm.OVERWRITE:
            existing_slides = list(deck.slides.all())
            if len(existing_slides) > 0:
                for slide in existing_slides:
                    slide.delete()
        # Actually import the images
        files = form.cleaned_data['files']
        for image in files:
            new_slide = Slide(deck=deck)
            new_slide.save()
            new_slide_element = SlideElement(
                css_class=form.cleaned_data["image_css_class"],
                order=0,
                slide=new_slide,
                image=image,
                body="",
            )
            new_slide_element.save()
        return HttpResponseRedirect(reverse_lazy('edit-deck', kwargs={'pk': deck.pk}))
