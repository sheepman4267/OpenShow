from django.views.generic import CreateView, UpdateView
from slides.models import Segment


class SegmentCreateView(CreateView):
    model = Segment
    fields = ['show', 'name', 'order']
    template_name = 'editor/new_segment_form.html'
    extra_context = {
        'object_type': 'Segment',
    }


class SegmentUpdateView(UpdateView):
    model = Segment
    fields = ['name', 'order', 'included_deck']
    template_name = 'editor/edit_segment_form.html'
