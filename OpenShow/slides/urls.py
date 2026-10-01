import django_eventstream
from django.urls import include, path

from . import views

urlpatterns = [
    # path('send_message', views.send_message),
    path('', views.IndexView.as_view(), name='slides-index'),
    path('get_message/<channel>', include(django_eventstream.urls)),
    path('<int:pk>', views.SlideView.as_view(), name='slide'),
    path('displays/<int:pk>', views.DisplayView.as_view(), name='display'),
    path('displays/<int:pk>/style', views.DisplayView.as_view(template_name='slides/display_style.css'), name='display-style'),
    path('displays/<int:pk>/transition', views.DisplayView.as_view(template_name='slides/transition.css'), name='display-transition'),
    path('displays/<int:pk>/clear', views.clear_slide, name='clear-slide'),
    path('displays/<int:pk>/remote', views.DisplayRemoteView.as_view(), name='display-remote'),
    path('show/<int:pk>', views.ShowView.as_view(), name='show'),
    path('show/<int:pk>/advance_mode', views.AdvanceModeView.as_view(), name='advance-mode'),
    path('show/<int:pk>/advance_loop', views.AdvanceLoopView.as_view(), name='advance-loop'),
    path('show/<int:pk>/select_displays', views.ShowDisplaySelectorView.as_view(), name='select-displays'),
    path('deck/<int:pk>', views.DeckView.as_view(), name='deck'),
    path('show_slide', views.ShowSlideView.as_view(), name='show-slide'),
    path('editor/', include('slides.editor.urls')),
]
