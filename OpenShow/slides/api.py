from ninja import Router, Schema
from .models import Slide, Show, Display, Deck
from django.shortcuts import get_object_or_404

router = Router()


class SlideAndShowSchema(Schema):
    slide_pk: int
    show_pk: int


class SlideAdvanceSchema(Schema):
    display_pk: int
    direction: str


class ShowDeckSchema(Schema):
    display_pk: int
    deck_pk: int


@router.post("show_slide")
def show_slide(request, slide_and_show: SlideAndShowSchema):
    slide = get_object_or_404(Slide, pk=slide_and_show.slide_pk)
    show = get_object_or_404(Show, pk=slide_and_show.show_pk)
    slide.send_to_display(show.displays.all(), show=show)
    return {"message": "OK"}


@router.post("show_deck")
def show_deck(request, data: ShowDeckSchema):
    display = get_object_or_404(Display, pk=data.display_pk)
    deck = get_object_or_404(Deck, pk=data.deck_pk)
    initial_slide = deck.slides.first()
    initial_slide.send_to_display([display, ])
    return {"message": "OK"}


@router.post("next_slide")
def next_slide(request, slide_advance: SlideAdvanceSchema):
    display = get_object_or_404(Display, pk=slide_advance.display_pk)
    display.advance_slide(slide_advance.direction)
