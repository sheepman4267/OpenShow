from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import DetailView, FormView, ListView, UpdateView
from django.template import loader
from .models import Slide, Display, Show, Deck

from .forms import SlideDisplayForm

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


class IndexView(ListView):
    model = Show
    template_name = 'slides/index.html'
    extra_context = {
        'deck_list': Deck.objects.all()
    }


class SlideView(DetailView):
    model = Slide
    template_name = 'slides/slide.html'


class DisplayView(DetailView):
    model = Display
    template_name = "slides/display.html"


class ShowView(DetailView):
    model = Show
    template_name = "slides/show.html"
    extra_context = {
        'shows': Show.objects.all(),
    }


class DeckView(DetailView):
    model = Deck
    template_name = "slides/deck.html"
    extra_context = {
        'decks': Deck.objects.all
    }


class ShowSlideView(FormView):
    form_class = SlideDisplayForm

    def form_valid(self, form):
        show = Show.objects.get(pk=form.cleaned_data['show_pk'])
        if form.cleaned_data['direction']:
            display = show.displays.all().first()
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
                                slide = current_segment.next_with_slides(form.cleaned_data['direction']).get_last_slide()
                            elif form.cleaned_data['direction'] == 'forward':
                                slide = current_segment.next_with_slides(form.cleaned_data['direction']).get_first_slide()
                        else:  # ..if current_slide.segment
                            current_segment = current_slide.segment
                            if form.cleaned_data['direction'] == 'reverse' and current_segment.included_deck:
                                slide = current_segment.included_deck.slides.last()
                            elif form.cleaned_data['direction'] == 'reverse':
                                slide = current_segment.next_with_slides(form.cleaned_data['direction']).get_last_slide()
                            elif form.cleaned_data['direction'] == 'forward':
                                slide = current_segment.next_with_slides(form.cleaned_data['direction']).get_first_slide()
                    except AttributeError:
                        slide = current_slide
                else:
                    slide = current_slide
        else:
            slide = Slide.objects.get(pk=form.cleaned_data['slide_pk'])
        slide.send_to_display(show.displays.all())
        return HttpResponseRedirect(reverse('show', kwargs={'pk':show.pk}))


class AdvanceModeView(UpdateView):
    model = Show
    fields = ['advance_between_segments']
