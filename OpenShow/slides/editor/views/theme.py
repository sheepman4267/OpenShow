from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from slides.models import Theme


class ThemeCreateView(CreateView):
    model = Theme
    template_name = 'editor/snippets/hx-simple_create_form.html'
    fields = ['name']
    extra_context = {
        'action': 'new-theme',
        'object_type': 'Theme',
    }


class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = 'editor/edit_theme.html'
    fields = ['name', 'css', 'default']
    extra_context = {
        'theme_list': Theme.objects.all
    }


class ThemeDeleteView(DeleteView):
    model = Theme
    success_url = reverse_lazy('slides-index')
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-theme',
    }
