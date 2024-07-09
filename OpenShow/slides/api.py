from ninja import Router, Schema
from .models import Slide, Show, Display
from django.shortcuts import get_object_or_404

router = Router()


class SlideAndShowSchema(Schema):
    slide_pk: int
    show_pk: int


class SlideAdvanceSchema(Schema):
    display_pk: int
    direction: str


@router.post("show_slide")
def show_slide(request, slide_and_show: SlideAndShowSchema):
    slide = get_object_or_404(Slide, pk=slide_and_show.slide_pk)
    show = get_object_or_404(Show, pk=slide_and_show.show_pk)
    slide.send_to_display(show.displays.all(), show=show)
    return {"message": "OK"}


@router.post("next_slide")
def next_slide(request, slide_advance: SlideAdvanceSchema):
    display = get_object_or_404(Display, pk=slide_advance.display_pk)
    display.advance_slide(slide_advance.direction)
