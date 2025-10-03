import requests
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.views.generic.detail import SingleObjectMixin

from slides.models import Show, RemoteSource
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
        print(form.cleaned_data)
        new_show = Show().import_json(title_prefix=form.cleaned_data.get('name_prefix'), json_string=form.cleaned_data.get('json_string'))
        return redirect(reverse('show', kwargs={'pk': new_show.pk}))

    def get_context_data(self, **kwargs):
        context = super(ShowJSONImportView, self).get_context_data(**kwargs)
        context['action'] = 'show-import-json'
        return context


class ShowRemoteImportView(FormView, SingleObjectMixin):
    form_class = ShowRemoteImportForm
    template_name = 'editor/remote_source/remote_source_import.html'
    model = RemoteSource

    def __init__(self, *args, **kwargs):
        super(self.__class__).__init__(*args, **kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(ShowRemoteImportView, self).get_context_data(**kwargs)
        context['action'] = 'remotesource-import-show'
        context['remote_source'] = self.object
        return context

    def get_form(self, *args, **kwargs):
        form = super(ShowRemoteImportView, self).get_form(*args, **kwargs)
        remote_source = self.get_object()
        form.fields['url'].choices = [
            (show['meta']['url'], show['meta']['name'])
            for show
            in remote_source.get_shows()['items']
        ]
        return form

    def form_valid(self, form):
        show = Show()
        json = requests.get(form.cleaned_data['url']).text
        show.import_json(title_prefix="Sunday/", json_string=json)
        return HttpResponseRedirect(show.get_absolute_url())


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
