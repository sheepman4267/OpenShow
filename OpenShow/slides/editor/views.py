from django.shortcuts import render, reverse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, FormView, DeleteView

from ..models import Show, Segment, Slide, SlideElement, Display, Deck, Theme

from .forms import DeleteSlideElementForm

# Create your views here.


class IndexView(ListView):
    queryset = Show.objects.all()
    template_name = 'editor/index.html'
    extra_context = {
        'deck_list': Deck.objects.all(),
        'theme_list': Theme.objects.all(),
        'display_list': Display.objects.all(),
    }


class ShowEditorView(DetailView):
    queryset = Show.objects.all()
    template_name = 'editor/show_editor.html'
    extra_context = {'display': Display.objects.all().first()}


class ShowCreateView(CreateView):
    model = Show
    fields = ['name']
    template_name = 'editor/new_show_form.html'


class SegmentCreateView(CreateView):
    model = Segment
    fields = ['show', 'name', 'order']
    template_name = 'editor/new_segment_form.html'


class SegmentUpdateView(UpdateView):
    model = Segment
    fields = ['name', 'order', 'included_deck']
    template_name = 'editor/edit_segment_form.html'


class SlideCreateView(CreateView):
    model = Slide
    fields = ['segment', 'deck']

    def form_valid(self, form):
        self.success_url = self.request.META['HTTP_REFERER']
        return super().form_valid(form)


class SlideElementCreateView(CreateView):
    model = SlideElement
    fields = ['css_class', 'body', 'order', 'image', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'new'}


class SlideElementUpdateView(UpdateView):
    model = SlideElement
    fields = ['css_class', 'body', 'order', 'image', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'edit'}


class SlideElementDeleteView(DeleteView):
    model = SlideElement
    template_name = 'editor/delete_element.html'
    form_class = DeleteSlideElementForm

    def form_valid(self, form):
        self.success_url = reverse('edit-slide', kwargs={"pk": form.cleaned_data["slide_pk"]})
        return super().form_valid(form)


class SlideEditView(DetailView):
    model = Slide
    template_name = 'editor/edit_slide.html'


class DeckCreateView(CreateView):
    model = Deck
    template_name = 'editor/new_deck_form.html'
    fields = ['name']


class DeckUpdateView(UpdateView):
    model = Deck
    template_name = 'editor/edit_deck.html'
    fields = ['name', 'theme']


class DeckEditorView(DetailView):
    queryset = Deck.objects.all()
    template_name = 'editor/deck_editor.html'
    extra_context = {'display': Display.objects.all().first()}