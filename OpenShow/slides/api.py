from ninja import Router, Schema
from .models import Slide, Show
from django.shortcuts import get_object_or_404

router = Router()


class SlideAndShowSchema(Schema):
    slide_pk: int
    show_pk: int


@router.post("show_slide")
def show_slide(request, slide_and_show: SlideAndShowSchema):
    slide = get_object_or_404(Slide, pk=slide_and_show.slide_pk)
    show = get_object_or_404(Show, pk=slide_and_show.show_pk)
    slide.send_to_display(show.displays.all(), show=show)
    return {"message": "OK"}
