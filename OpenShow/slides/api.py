from ninja import Router
from .models import Slide, Show
from django.shortcuts import get_object_or_404

router = Router()


@router.post("show_slide")
def show_slide(request, slide_pk, show_pk):
    slide = get_object_or_404(Slide, pk=slide_pk)
    show = get_object_or_404(Show, pk=show_pk)
    slide.send_to_display(show.displays.all(), show=show)
