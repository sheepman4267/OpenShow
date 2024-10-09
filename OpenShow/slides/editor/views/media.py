from neapolitan.views import CRUDView

from slides.models import MediaObject


class MediaObjectCRUDView(CRUDView):
    model = MediaObject
    fields = [
        'title',
        'media_type',
        'raw_file',
        'embed_url',
        #'autoplay',  # Uncomment this once it will be useful for something
    ]
