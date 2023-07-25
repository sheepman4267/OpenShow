# from slides.models import Deck, Segment
#
# from OpenShow.slides.models import Deck
#
#
# def parse_element(element_pk, element_json):
#     element = Segment.objects.get(pk=element_pk)
#     element_header = element_json['value']['header']
#     if 'hymn' in element_header.lower():
#         element.included_deck = Deck.objects.filter(name__contains=element_json['value'][''])
#
