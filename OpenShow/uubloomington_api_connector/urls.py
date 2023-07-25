from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='uubloomington_api_connector/index.html'), name='uucb-api-index'),
    path('create-show-from-oos/', CreateShowFromOOSView.as_view(), name='create-show-from-oos'),
]