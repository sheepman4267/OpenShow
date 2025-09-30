from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from neapolitan.views import CRUDView, Role

from slides.models import RemoteSource


class RemoteSourceCRUDView(CRUDView):
    model = RemoteSource
    fields = [
        'name',
        'source_url',
        'refresh_every',
    ]

    def get_success_url(self):
        if self.role is Role.DELETE:
            success_url = reverse('slides-index')
        else:
            success_url = super(self.__class__, self).get_success_url()
        return success_url

    def detail(self, request, *args, **kwargs):
        """GET handler for the detail view."""
        self.object = self.get_object()
        context = self.get_context_data()
        context['previous_page'] = 'slides-index'
        return self.render_to_response(context)

    def get_template_names(self):
        return [
            f"editor/remote_source/remote_source{self.template_name_suffix}.html",
        ]


def refresh_source(request, pk):
    remote_source = get_object_or_404(RemoteSource, pk=pk)
    remote_source.get_metadata()
    return HttpResponseRedirect(reverse('remotesource-detail', kwargs={'pk': pk}))