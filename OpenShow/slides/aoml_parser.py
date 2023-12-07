# Functions for parsing (and generally tolerating) AOML - "Awful OpenShow Markup Language"
from slides.models import Slide, SlideElement


class InvalidArgumentException(Exception):
    pass


def parse_element_body(markup:str) -> str:
    """
    Parse AOML inline markup and return the final element body string
    :param markup:
    :return:
    """
    body = markup
    body = body.replace("\\", "<br>")
    return body


def parse_element(markup: str) -> SlideElement:
    """
    Parse an AOML-formatted slide element, returning a SlideElement object which can be saved in the database
    :param markup:
    :return: SlideElement
    """
    print('MARKUP'+markup+str(len(markup)))
    markup = markup.split('||')
    if len(markup) > 2:
        raise InvalidArgumentException(f'Invalid markup: too many || tokens in element {markup}')
    css_class = markup[0]
    body = parse_element_body(markup[1])
    return SlideElement(css_class=css_class, body=body)


def parse_slide(markup: str) -> list:
    """
    Parse an AOML-formatted slide, returning a list of SlideElement objects which can be assigned a Slide, then saved in the database.
    :param markup:
    :return: list
    """
    return [
        parse_element(element)
        for element
        in markup.split('>>')
        if len(element.strip()) > 0
    ]


def parse_markup(markup: str) -> list:
    """
    Parse an AOML document containing slides and their elements, returning a list of AOML-formatted slide strings.
    :param markup:
    :return:
    """
    return [
        slide for slide in markup.split('~~')
    ]
