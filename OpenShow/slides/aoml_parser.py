# Functions for parsing (and generally tolerating) AOML - "Awful OpenShow Markup Language"
from dataclasses import dataclass
from typing import List
import yaml

from slides.models import Slide, SlideElement, Image, MediaObject


class InvalidArgumentException(Exception):
    pass


@dataclass
class AOMLSlideIntermediate:
    """An intermediate data type for use in parsing AOML to slides and back again"""
    elements: List[SlideElement]
    cue: str or None = None


def parse_element_body(markup:str) -> str:
    """
    Parse AOML inline markup and return the final element body string
    :param markup:
    :return:
    """
    body = markup
    body = "".join(body.splitlines())
    body = body.replace("\\", "<br>")
    return body


def parse_element(markup: str) -> SlideElement:
    """
    Parse an AOML-formatted slide element, returning a SlideElement object which can be saved in the database
    :param markup:
    :return: SlideElement
    """
    markup = markup.split('||')
    if len(markup) > 4:
        raise InvalidArgumentException(f'Invalid markup: too many || tokens in element {markup}')
    css_class = markup[0]
    body = parse_element_body(markup[-1])
    element = SlideElement(css_class=css_class, body=body)
    for media in markup[1:-1]:
        # Note: This for loop only runs if len(markup) > 3.
        media = media.strip('\r').strip('\n').split(':')
        if len(media) > 2:
            raise InvalidArgumentException(f'Invalid markup: malformed media token in element {markup}')
        media_type = media[0]
        match media_type:
            case "image":
                element.image_object = Image.objects.filter(file_hash=media[1]).first()
                if element.image_object is None:
                    element.missing_image_object = True
            case "media":
                element.media_object = MediaObject.objects.filter(file_hash=media[1]).first()
                if element.media_object is None:
                    element.missing_media_object = True
    return element


def parse_slide(markup: str) -> AOMLSlideIntermediate:
    """
    Parse an AOML-formatted slide, returning a dict describing an entire slide, including elements. The key "elements" is a list of SlideElement objects which can be assigned a Slide, then saved in the database.
    :param markup:
    :return: list
    """
    split_markup = markup.split('##')
    if len(split_markup) > 1:
        element_markup = split_markup[-1]
        slide_metadata = yaml.safe_load(split_markup[0])
        cue = slide_metadata.get('cue')
    else:
        element_markup = split_markup[-1]
        cue = None
    elements = [
        parse_element(element)
        for element
        in element_markup.split('>>')
        if len(element.strip()) > 0
    ]
    return AOMLSlideIntermediate(
        elements=elements,
        cue=cue,
    )


def parse_markup(markup: str) -> list:
    """
    Parse an AOML document containing slides and their elements, returning a list of AOML-formatted slide strings.
    :param markup:
    :return:
    """
    return [
        slide for slide in markup.split('~~')
    ]
