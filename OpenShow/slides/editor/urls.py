from django.urls import path
from .views import *

from slides.editor.views.index import IndexView
from slides.editor.views.show import ShowEditorView, ShowCreateView, ShowDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='editor_index'),
    path('show/<int:pk>', ShowEditorView.as_view(), name='edit-show'),
    path('show/new', ShowCreateView.as_view(), name='new-show'),
    path('show/<int:pk>/delete', ShowDeleteView.as_view(), name='delete-show'),
    path('segment/<int:pk>', SegmentUpdateView.as_view(), name='edit-segment'),
    path('segment/new', SegmentCreateView.as_view(), name='new-segment'),
    path('slide/new', SlideCreateView.as_view(), name='new-slide'),
    path('slide/<int:pk>', SlideEditView.as_view(), name='edit-slide'),
    path('slide/<int:pk>/delete', SlideDeleteView.as_view(), name='delete-slide'),
    path('slide/element/new', SlideElementCreateView.as_view(), name='new-element'),
    path('slide/element/<int:pk>', SlideElementUpdateView.as_view(), name='edit-element'),
    path('slide/element/delete/<int:pk>', SlideElementDeleteView.as_view(), name='delete-element'),
    path('slide/element/<int:pk>/text-edit', EditSlideElementTextView.as_view(), name='edit-element-text'),
    path('slide/reorder', ChangeSlideOrderView.as_view(), name='reorder-slide'),
    path('deck/new', DeckCreateView.as_view(), name='new-deck'),
    path('deck/<int:pk>', DeckEditorView.as_view(), name='edit-deck'),
    path('deck/<int:pk>/delete', DeckDeleteView.as_view(), name='delete-deck'),
    path('deck/<int:pk>/push-cues', push_deck_cues, name='push-deck-cues'),
    path('deck/<int:pk>/push-text', push_deck_slide_text, name='push-deck-text'),
    path('deck/<int:pk>/pull-aoml', pull_aoml_text, name='pull-aoml-text'),
    path('theme/new', ThemeCreateView.as_view(), name='new-theme'),
    path('theme/<int:pk>', ThemeUpdateView.as_view(), name='edit-theme'),
    path('theme/<int:pk>/delete', ThemeDeleteView.as_view(), name='delete-theme'),
    path('lorem/<int:words>/<str:css_class>', generate_lorem, name='lorem'),
    path('show/<int:pk>/set-theme/', SetThemeView.as_view(), name='set-theme'),
    path('show/check-theme-compatibility', check_theme_compatibility, name='check-theme-compatibility'),
    path('transition', TransitionEditorIndexView.as_view(), name='transition-editor'),
    path('transition/<int:pk>', TransitionEditorView.as_view(), name='edit-transition'),
    path('transition/new', TransitionCreateView.as_view(), name='new-transition'),
    path('transition/keyframe/new', TransitionKeyframeCreateView.as_view(), name='new-keyframe'),
    path('transition/keyframe/<int:pk>', TransitionKeyframeUpdateView.as_view(), name='edit-keyframe'),
]