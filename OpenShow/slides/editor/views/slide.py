from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from slides.models import Slide
from slides.editor.forms import ChangeSlideOrderForm
import slides.aoml_parser as aoml


class SlideCreateView(CreateView):
    model = Slide
    fields = ['segment', 'deck']


class SlideTextEditView(DetailView):
    model = Slide
    template_name = 'editor/slide/wysiwyg/iframe-slide-preview.html'


class SlideEditView(UpdateView):
    model = Slide
    fields = ['transition', 'transition_duration', 'auto_advance', 'auto_advance_duration']
    template_name = 'editor/slide/edit_slide.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.object.deck:
            context['edit_show_or_deck_template'] = 'editor/deck_editor.html'
            context['deck'] = self.object.deck
        elif self.object.segment:
            context['edit_show_or_deck_template'] = 'editor/show_editor.html'
            context['show'] = self.object.segment.show
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


def duplicate_slide(request, pk):
    existing_slide = Slide.objects.get(pk=pk)
    slide_markup = existing_slide.pull_aoml()
    slide_intermediate = aoml.parse_slide(slide_markup)
    next_slide = existing_slide.next('forward')
    if next_slide:
        order = existing_slide.order + ((next_slide.order - existing_slide.order) / 2)
    else:
        order = existing_slide.order + 10
    new_slide = Slide(deck=existing_slide.deck, segment=existing_slide.segment, cue=slide_intermediate.cue, order=order)
    new_slide.save()
    for element in slide_intermediate.elements:
        element.slide = new_slide
        element.save()
    return HttpResponseRedirect(new_slide.get_absolute_url())