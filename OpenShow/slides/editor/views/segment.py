from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from slides.models import Segment
from slides.editor.forms import UpdateSegmentForm, ChangeSegmentOrderForm


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


class SegmentDeleteView(DeleteView):
    model = Segment
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-segment',
    }

    def get_success_url(self):
        success_url = reverse_lazy('edit-show', kwargs={"pk": self.object.show.pk})
        return success_url


class ChangeSegmentOrderView(FormView):
    form_class = ChangeSegmentOrderForm

    def __init__(self):
        self.moved_segment = None
        super().__init__()

    def form_valid(self, form):
        self.moved_segment = Segment.objects.get(pk=form.cleaned_data['moved_segment_pk'])
        if form.cleaned_data['next_segment_pk']:
            next_segment = Segment.objects.get(pk=form.cleaned_data['next_segment_pk'])
            previous_segment = Segment.objects.filter(
                show=self.moved_segment.show,
                order__lt=next_segment.order,
            ).last()
            if previous_segment:
                order_difference = next_segment.order - previous_segment.order
                self.moved_segment.order = next_segment.order - (order_difference / 2)
                self.moved_segment.save()
            else:
                self.moved_segment.order = next_segment.order - 1
                self.moved_segment.save()
        else:
            self.moved_segment.order = self.moved_segment.show.segments.last().order + 10
            self.moved_segment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.moved_segment.show.get_absolute_url()