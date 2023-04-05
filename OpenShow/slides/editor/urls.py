from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='editor_index'),
    path('show/<int:pk>', ShowEditorView.as_view(), name='edit-show'),
    path('show/new', ShowCreateView.as_view(), name='new-show'),
    path('segment/new', SegmentCreateView.as_view(), name='new-segment'),
    path('slide/new', SlideCreateView.as_view(), name='new-slide'),
    path('slide/<int:pk>', SlideEditView.as_view(), name='edit-slide'),
    path('slide/element/new', SlideElementCreateView.as_view(), name='new-element'),
    path('slide/element/<int:pk>', SlideElementUpdateView.as_view(), name='edit-element'),
    path('slide/element/delete/<int:pk>', SlideElementDeleteView.as_view(), name='delete-element'),
    path('deck/new', DeckCreateView.as_view(), name='new-deck'),
    path('deck/<int:pk>', DeckEditorView.as_view(), name='edit-deck'),
]