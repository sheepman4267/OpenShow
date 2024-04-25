from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Projector

# Create your views here.


class ProjectorListView(ListView):
    model = Projector
    template_name = 'pjlink_integration/list.html'
    extra_context = {
        'previous_page': 'index',
    }


class ProjectorCreateView(CreateView):
    model = Projector
    template_name = 'pjlink_integration/new.html'
    success_url = reverse_lazy('pjlink-index')
    fields = [
        'name',
        'address',
    ]


class ProjectorUpdateView(UpdateView):
    model = Projector
    template_name = 'pjlink_integration/edit.html'
    success_url = reverse_lazy('pjlink-index')
    fields = [
        'name',
        'address',
    ]


def power_on(request, pk):
    proj = get_object_or_404(Projector, pk=pk)
    proj.power_on()
    return redirect(reverse('pjlink-index'))


def power_off(request, pk):
    proj = get_object_or_404(Projector, pk=pk)
    proj.power_off()
    return redirect(reverse('pjlink-index'))
