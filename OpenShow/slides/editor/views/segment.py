from django.views.generic import CreateView, UpdateView
from slides.models import Segment
from slides.editor.forms import UpdateSegmentForm


class SegmentCreateView(CreateView):
    model = Segment
    fields = ['show', 'name', 'order']
    template_name = 'editor/segment/new_segment_form.html'
    extra_context = {
        'object_type': 'Segment',
    }


class SegmentUpdateView(UpdateView):
    model = Segment
    template_name = 'editor/segment/edit_segment_form.html'
    form_class = UpdateSegmentForm

    def get_context_data(self, **kwargs):
        context = super(SegmentUpdateView, self).get_context_data(**kwargs)
        context['show'] = self.object.show
        return context

    def get_success_url(self):
        return self.object.show.get_absolute_url()