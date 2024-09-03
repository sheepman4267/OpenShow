from django.urls import path

from slides.editor.views.index import IndexView
from slides.editor.views.show import ShowEditorView, ShowCreateView, ShowDeleteView, SetThemeView, check_theme_compatibility
from slides.editor.views.segment import SegmentCreateView, SegmentUpdateView
from slides.editor.views.slide import SlideCreateView, SlideEditView, SlideDeleteView, ChangeSlideOrderView
from slides.editor.views.slide_element import SlideElementCreateView, SlideElementDeleteView, \
    SlideElementDeleteView, SlideElementUpdateTextView, SlideElementUpdateCSSClassView, SlideElementUpdateImageView, \
    SlideElementUpdateVideoView, ChangeSlideElementOrderView
from slides.editor.views.deck import DeckCreateView, DeckEditorView, DeckDeleteView, push_deck_cues, push_deck_slide_text, pull_aoml_text
from slides.editor.views.theme import ThemeUpdateView, ThemeCreateView, ThemeDeleteView
from slides.editor.views.utils import generate_lorem
from slides.editor.views.transition import TransitionEditorView, TransitionCreateView, TransitionKeyframeCreateView, TransitionKeyframeUpdateView, TransitionEditorIndexView


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
    path('slide/element/delete/<int:pk>', SlideElementDeleteView.as_view(), name='delete-element'),
    path('slide/element/<int:pk>/text-edit', SlideElementUpdateTextView.as_view(), name='edit-element-text'),
    path('slide/element/<int:pk>/css-class', SlideElementUpdateCSSClassView.as_view(), name='edit-element-css-class'),
    path('slide/element/<int:pk>/image', SlideElementUpdateImageView.as_view(), name='edit-element-image'),
    path('slide/element/<int:pk>/video', SlideElementUpdateVideoView.as_view(), name='edit-element-video'),
    path('slide/element/reorder', ChangeSlideElementOrderView.as_view(), name='reorder-element'),
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