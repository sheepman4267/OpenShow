from django.urls import path, include
from . import views
import django_eventstream

urlpatterns = [
    # path('send_message', views.send_message),
    path('get_message/<channel>', include(django_eventstream.urls)),
    path('<int:pk>', views.SlideView.as_view(), name='slide'),
    path('displays/<int:pk>', views.DisplayView.as_view(), name='display'),
    path('show/<int:pk>', views.ShowView.as_view(), name='show'),
    path('show_slide', views.ShowSlideView.as_view(), name='show-slide'),
    # path('send_slide/<int:slide_pk>/<int:display_pk>', views.send_slide_to_display),
    path('editor/', include('slides.editor.urls')),
]