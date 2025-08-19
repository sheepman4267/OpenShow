from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from slides.models import Show
from slides.editor.forms import SetThemeForm
from ..forms import ShowRemoteImportForm, ShowJSONImportForm

class ShowEditorView(UpdateView):
    model = Show
    fields = [
        'name',
        'displays',
        'advance_between_segments',
        'advance_loop',
    ]
    template_name = 'editor/show_editor.html'


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


class SetThemeView(UpdateView):
    model = Show
    form_class = SetThemeForm
    template_name = 'editor/set_theme.html'


class ShowJSONImportView(FormView):
    form_class = ShowJSONImportForm
    template_name = 'editor/snippets/hx-simple_create_form.html'

    def form_valid(self, form):
        Show.import_json(form.cleaned_data.get('name_prefix'), form.cleaned_data.get('json_string'))

    def get_context_data(self, **kwargs):
        context = super(ShowJSONImportView, self).get_context_data(**kwargs)
        context['action'] = 'show-import-json'
        return context


class ShowRemoteImportView(FormView):
    form_class = ShowRemoteImportForm
    template_name = 'editor/snippets/hx-simple_create_form.html'

    def get(self, request, *args, **kwargs):
        form = self.get_form()



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
