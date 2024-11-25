from django.views.generic import CreateView, FormView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from slides.models import Slide
from slides.editor.forms import ChangeSlideOrderForm


class SlideCreateView(CreateView):
    model = Slide
    fields = ['segment', 'deck']

    def form_valid(self, form):
        self.success_url = self.request.META['HTTP_REFERER']
        return super().form_valid(form)


class SlideTextEditView(DetailView):
    model = Slide
    template_name = 'editor/iframe-slide-preview.html'


class SlideEditView(UpdateView):
    model = Slide
    fields = ['transition', 'transition_duration', 'auto_advance', 'auto_advance_duration', 'order']
    template_name = 'editor/edit_slide.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.object.deck:
            context['edit_show_or_deck_template'] = 'editor/deck_editor.html'
            context['deck'] = self.object.deck
        elif self.object.segment:
            context['edit_show_or_segment_template'] = 'editor/show_editor.html'
        return context

class SlideDeleteView(DeleteView):
    model = Slide
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-slide',
    }

    def get_success_url(self):
        if self.object.deck:
            success_url = reverse_lazy('edit-deck', kwargs={"pk": self.object.deck.pk})
        elif self.object.segment:
            success_url = reverse_lazy('edit-show', kwargs={"pk": self.object.segment.show.pk})
        else:
            success_url = reverse_lazy('index')
        return success_url




class ChangeSlideOrderView(FormView):
    form_class = ChangeSlideOrderForm

    def __init__(self):
        self.moved_slide = None
        super().__init__()

    def form_valid(self, form):
        self.moved_slide = Slide.objects.get(pk=form.cleaned_data['moved_slide_pk'])
        if form.cleaned_data['next_slide_pk']:
            next_slide = Slide.objects.get(pk=form.cleaned_data['next_slide_pk'])
            previous_slide = Slide.objects.filter(
                deck=self.moved_slide.deck,
                order__lt=next_slide.order,
            ).last()
            if previous_slide:
                order_difference = next_slide.order - previous_slide.order
                self.moved_slide.order = next_slide.order - (order_difference / 2)
                self.moved_slide.save()
            else:
                self.moved_slide.order = next_slide.order - 1
                self.moved_slide.save()
        else:
            self.moved_slide.order = self.moved_slide.deck_or_segment().slides.last().order + 10
            self.moved_slide.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.moved_slide.deck_or_segment().get_absolute_url()
