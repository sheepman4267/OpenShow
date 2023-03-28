from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.generic import DetailView, FormView
from django.template import loader
from .models import Slide, Display, Show

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


class SlideView(DetailView):
    model = Slide
    template_name = 'slides/slide.html'


class DeckView(DetailView):
    pass


class DisplayView(DetailView):
    model = Display
    template_name = "slides/display.html"


class ShowView(DetailView):
    model = Show
    template_name = "slides/show.html"


class ShowSlideView(FormView):
    form_class = SlideDisplayForm

    def form_valid(self, form):
        slide = Slide.objects.get(pk=form.cleaned_data['slide_pk'])
        show = Show.objects.get(pk=form.cleaned_data['show_pk'])
        slide.send_to_display(show.displays.all())
        return HttpResponseRedirect(reverse('show', kwargs={'pk':show.pk}))