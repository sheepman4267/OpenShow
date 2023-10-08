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
    success_url = reverse_lazy('create-show-from-oos')

    def form_valid(self, form):
        oos = json.loads(
            urlopen(f"https://uubloomington.org/api/v2/pages/{form.cleaned_data['order_of_service_id']}/?type=services.OrderOfService").read()
        )
        new_show = Show(name=f"Sunday/{oos['date']}")
        new_show.save()
        for idx, element in enumerate(oos['program']):
            if element['type'] != 'element':
                continue
            else:
                new_segment = Segment(name=element['value']['header'], show=new_show, order=(idx * 10))
                new_segment.save()
        return super().form_valid(self)