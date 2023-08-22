from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import DetailView, CreateView, ListView, UpdateView, FormView, DeleteView

from ..models import Show, Segment, Slide, SlideElement, Display, Deck, Theme, Transition, TransitionKeyframe

from .forms import DeleteSlideElementForm, SetThemeForm

import lorem

# Create your views here.


class IndexView(ListView):
    queryset = Show.objects.all()
    template_name = 'editor/index.html'
    extra_context = {
        'deck_list': Deck.objects.all,
        'theme_list': Theme.objects.all,
        'display_list': Display.objects.all,
    }


class ShowEditorView(DetailView):
    queryset = Show.objects.all()
    template_name = 'editor/show_editor.html'
    # extra_context = {'display': Display.objects.all().first()}


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
    fields = ['css_class', 'body', 'order', 'image', 'video', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'new'}


class SlideElementUpdateView(UpdateView):
    model = SlideElement
    fields = ['css_class', 'body', 'order', 'image','video', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'edit'}


class SlideElementDeleteView(DeleteView):
    model = SlideElement
    template_name = 'editor/delete_element.html'
    form_class = DeleteSlideElementForm

    def form_valid(self, form):
        self.success_url = reverse('edit-slide', kwargs={"pk": form.cleaned_data["slide_pk"]})
        return super().form_valid(form)


class SlideEditView(UpdateView):
    model = Slide
    fields = ['transition']
    template_name = 'editor/edit_slide.html'


class DeckCreateView(CreateView):
    model = Deck
    template_name = 'editor/simple_create_form.html'
    fields = ['name']
    extra_context = {'action': 'new-deck'}


class DeckUpdateView(UpdateView):
    model = Deck
    template_name = 'editor/edit_deck.html'
    fields = ['name', 'theme']


class DeckEditorView(UpdateView):
    queryset = Deck.objects.all()
    model = Deck
    fields = ['name', 'theme']
    template_name = 'editor/deck_editor.html'
    # extra_context = {'display': Display.objects.all().first()}


class ThemeCreateView(CreateView):
    model = Theme
    template_name = 'editor/simple_create_form.html'
    fields = ['name']
    extra_context = {'action': 'new-theme'}


class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = 'editor/edit_theme.html'
    fields = ['name', 'css']
    extra_context = {
        'theme_list': Theme.objects.all
    }


class SetThemeView(UpdateView):
    model = Show
    # fields = ['theme']
    form_class = SetThemeForm
    template_name = 'editor/set_theme.html'


# class CheckThemeCompatibilityView(FormView):
#     form_class = SetThemeForm
#     template_name = 'editor/show_compatibility_snippet.html'
#
#     def form_valid(self, form):
#         show = Show.objects.get(form.cleaned_data['show_pk'])
#         missing = show.check_compatibility(form.cleaned_data['theme'])
#         if len(missing) <= 0:
#             missing = None
#         return render(self.request, 'editor/show_compatibility_snippet.html', {
#             'missing': missing
#         })


def generate_lorem(request, css_class:str, words:int):
    return render(request, 'editor/lorem.html',
                  context={
                      'css_class': css_class,
                      'lorem': lorem.get_word(count=words)
                  })


def check_theme_compatibility(request):
    form = SetThemeForm(request.POST)
    if form.is_valid():
        show = Show.objects.get(pk=form.cleaned_data['show_pk'])
        theme = form.cleaned_data['theme']
        missing = show.check_compatibility(theme)
        if len(missing) == 0:
            missing = None
        return render(request, 'editor/show_compatibility_snippet.html', {
            'missing': missing,
        })


class TransitionEditorIndexView(ListView):
    queryset = Transition.objects.all()
    template_name = 'editor/transition_editor.html'
    extra_context = {
        'transition_list': Transition.objects.all()
    }


class TransitionEditorView(DetailView):
    model = Transition
    template_name = 'editor/transition_editor.html'
    extra_context = {
        'transition_list': Transition.objects.all
    }


class TransitionCreateView(CreateView):
    model = Transition
    fields = ["name"]
    template_name = "editor/simple_create_form.html"
    extra_context = {
        'action': 'new-transition',
    }


class TransitionKeyframeCreateView(CreateView):
    model = TransitionKeyframe
    fields = ["transition", "marker", "css", "out"]
    template_name = "editor/edit_keyframe.html"
    extra_context = {
        'action': 'new-keyframe',
    }


class TransitionKeyframeUpdateView(UpdateView):
    model = TransitionKeyframe
    fields = ["marker", "css"]
    template_name = "editor/edit_keyframe.html"
    extra_context = {
        'action': 'edit-keyframe',
    }
