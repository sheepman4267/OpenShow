from django.urls import path

from .views import DeckFromImagesFormView

urlpatterns = [
    path('new', DeckFromImagesFormView.as_view(), name='deck-from-images')
]