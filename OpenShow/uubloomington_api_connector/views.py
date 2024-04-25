from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import CreateShowFromOOSForm
from slides.models import Show, Segment

from urllib.request import urlopen
import json

# Create your views here.


class CreateShowFromOOSView(FormView):
    form_class = CreateShowFromOOSForm
    template_name = 'uubloomington_api_connector/create_show_from_oos.html'
    # success_url = reverse_lazy('edit-show', pk=object.pk)
    extra_context = {
        'previous_page': 'index',
    }

    def __init__(self):
        self.new_show = None
        super().__init__()

    def get_success_url(self):
        return reverse_lazy('edit-show', kwargs={'pk': self.new_show.pk})

    def form_valid(self, form):
        oos = json.loads(
            urlopen(f"https://uubloomington.org/api/v2/pages/{form.cleaned_data['order_of_service_id']}/?type=services.OrderOfService").read()
        )
        new_show = Show(name=f"Sunday/{oos['date']}")
        new_show.save()
        self.new_show = new_show
        for idx, element in enumerate(oos['program']):
            if element['type'] != 'element':
                continue
            else:
                new_segment = Segment(name=element['value']['header'], show=new_show, order=(idx * 10))
                new_segment.save()
        return super().form_valid(self)