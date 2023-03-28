from django.shortcuts import render, reverse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, FormView

from ..models import Show, Segment, Slide, SlideElement, Display

# Create your views here.


class IndexView(ListView):
    queryset = Show.objects.all()
    template_name = 'editor/index.html'


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


class SlideCreateView(CreateView):
    model = Slide
    fields = ['segment']

    def form_valid(self, form):
        self.success_url = self.request.META['HTTP_REFERER']
        return super().form_valid(form)


class SlideElementCreateView(CreateView):
    model = SlideElement
    fields = ['name', 'css_class', 'body', 'order', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'new'}


class SlideElementUpdateView(UpdateView):
    model = SlideElement
    fields = ['name', 'css_class', 'body', 'order', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'edit'}


class SlideEditView(DetailView):
    model = Slide
    template_name = 'editor/edit_slide.html'
