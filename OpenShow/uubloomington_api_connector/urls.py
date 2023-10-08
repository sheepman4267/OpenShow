from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('create-show-from-oos/', CreateShowFromOOSView.as_view(), name='create-show-from-oos'),
]