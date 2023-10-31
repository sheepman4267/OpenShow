from django.urls import path
from .views import *

urlpatterns = [
    path('', ProjectorListView.as_view(), name='pjlink-index'),
    path('new', ProjectorCreateView.as_view(), name='new-projector'),
    path('edit/<int:pk>', ProjectorUpdateView.as_view(), name='edit-projector'),
    path('power/<int:pk>/on', power_on, name='power-on'),
    path('power/<int:pk>/off', power_off, name='power-off'),
]
