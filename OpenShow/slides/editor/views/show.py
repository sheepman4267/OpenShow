from django.views.generic import DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from slides.models import Show

class ShowEditorView(DetailView):
    queryset = Show.objects.all()
    template_name = 'editor/show_editor.html'
    # extra_context = {'display': Display.objects.all().first()}


class ShowCreateView(CreateView):
    model = Show
    fields = ['name']
    template_name = 'editor/snippets/hx-simple_create_form.html'
    extra_context = {
        'action': 'new-show',
        'object_type': 'Show',
    }


class ShowDeleteView(DeleteView):
    model = Show
    success_url = reverse_lazy('slides-index')
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-show',
    }