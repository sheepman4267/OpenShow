from datetime import timedelta

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, UpdateView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.template import loader
from .models import Slide, Display, Show, Deck, Transition, Theme

from .forms import SlideDisplayForm, ShowDisplaySelectorForm

# import htmlmin # Was for the old send slide to display stuff

# Create your views here.
from django_eventstream import send_event
from django.shortcuts import HttpResponse


# This approach doesn't work well due to many extra characters being inserted into the HTML/CSS.
# def send_slide_to_display(request, slide, display):
#     slide_template = loader.get_template('slides/slide.html')
#     context = {
#         'slide': Slide.objects.get(pk=slide),
#     }
#     rendered_slide = htmlmin.minify(slide_template.render(context, request),remove_empty_space=True,remove_all_empty_space=True).replace('\n','')
#     print(rendered_slide)
#     send_event('test', f'display-{display}', rendered_slide)


class IndexView(TemplateView):
    model = Show
    template_name = 'slides/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['show_list'] = Show.objects.all()
        context['deck_list'] = Deck.objects.all()
        context['theme_list'] = Theme.objects.all()
        context['display_list'] = Display.objects.all()
        context['transition_list'] = Transition.objects.all()
        context['previous_page'] = 'index'
        return context


class SlideView(DetailView):
    model = Slide
    template_name = 'slides/slide.html'


@method_decorator(xframe_options_sameorigin, "get")
class DisplayView(DetailView):
    model = Display
    template_name = "slides/display.html"


class ShowView(DetailView):
    model = Show
    template_name = "slides/show.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['display_selector_form'] = ShowDisplaySelectorForm(instance=context['show'])
        context['shows'] = Show.objects.all()
        context['previous_page'] = 'slides-index'
        return context


class ShowDisplaySelectorView(UpdateView):
    model = Show
    form_class = ShowDisplaySelectorForm


class DeckView(DetailView):
    model = Deck
    template_name = "slides/deck.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decks'] = Deck.objects.all()
        context['display_list'] = Display.objects.all()
        context['previous_page'] = 'slides-index'
        return context


class ShowSlideView(FormView):
    form_class = SlideDisplayForm

    def form_valid(self, form):
        if form.cleaned_data['display_pk_multiple']:
            display_pks = form.cleaned_data['display_pk_multiple'].split(',')
            displays = [Display.objects.get(pk=int(display_pk)) for display_pk in display_pks]
            slide = Slide.objects.get(pk=form.cleaned_data['slide_pk'])
            slide.send_to_display(displays, show=displays[0].current_show)
            return HttpResponseRedirect(reverse('deck', kwargs={'pk': slide.deck.pk}))
        show = Show.objects.get(pk=form.cleaned_data['show_pk'])
        if form.cleaned_data['direction']:
            display = show.displays.all().first()
            if display.previous_slide and display.current_slide.auto_advance:
                if timezone.now() - \
                        display.slide_changed_at < \
                        timedelta(seconds=display.previous_slide.auto_advance_duration):
                    # Abort and continue silently if we're getting a "next slide" directive and
                    # the previous slide's auto_advance_duration has not passed
                    # Manually selecting a different slide will override this.
                    return HttpResponseRedirect(reverse('show', kwargs={'pk': show.pk}))
            current_slide = display.current_slide
            slide = current_slide.next(form.cleaned_data['direction'])
            next_segment = None
            if not slide:
                if show.advance_between_segments:
                    try:  # TODO: review this horrible try/except block
                        if current_slide.deck:
                            current_segment = show.segments.filter(included_deck=current_slide.deck).first()
                            if current_segment.slides.first() and form.cleaned_data['direction'] == 'forward':
                                slide = current_segment.slides.first()
                            elif form.cleaned_data['direction'] == 'reverse':
                                slide = current_segment.next_with_slides(
                                    form.cleaned_data['direction']).get_last_slide()
                            elif form.cleaned_data['direction'] == 'forward':
                                slide = current_segment.next_with_slides(
                                    form.cleaned_data['direction']).get_first_slide()
                        else:  # ..if current_slide.segment
                            current_segment = current_slide.segment
                            if form.cleaned_data['direction'] == 'reverse' and current_segment.included_deck:
                                slide = current_segment.included_deck.slides.last()
                            elif form.cleaned_data['direction'] == 'reverse':
                                slide = current_segment.next_with_slides(
                                    form.cleaned_data['direction']).get_last_slide()
                            elif form.cleaned_data['direction'] == 'forward':
                                slide = current_segment.next_with_slides(
                                    form.cleaned_data['direction']).get_first_slide()
                    except AttributeError:
                        slide = current_slide
                elif show.advance_loop:
                    if form.cleaned_data['direction'] == 'reverse':
                        if current_slide.deck:
                            slide = current_slide.deck.slides.last()
                        else:
                            slide = current_slide.segment.slides.last()
                    elif form.cleaned_data['direction'] == 'forward':
                        if current_slide.deck:
                            slide = current_slide.deck.slides.first()
                        else:
                            slide = current_slide.segment.slides.first()
                else:
                    slide = current_slide
        else:
            slide = Slide.objects.get(pk=form.cleaned_data['slide_pk'])
        slide.send_to_display(show.displays.all(), show=show)
        return HttpResponseRedirect(reverse('show', kwargs={'pk': show.pk}))


class AdvanceModeView(UpdateView):
    model = Show
    fields = ['advance_between_segments']


class AdvanceLoopView(UpdateView):  # TODO: Combine this and the above view, make this all one proper Django form
    model = Show
    fields = ['advance_loop']
