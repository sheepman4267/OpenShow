from django.core.management.base import BaseCommand
from slides.editor.tasks import thumbnail_video
from slides.models import MediaObject


class Command(BaseCommand):
    help = 'Schedules MediaObjects with media type "Video" and no thumbnail image for thumbnail processing'

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Schedule all videos for thumbnail processing (e.g. to reflect a change to how thumbnails are generated)",
        )
        parser.add_argument("--verbose", action="store_true", help="Verbose output")

    def handle(self, *args, **options):
        if options["all"]:
            media_needing_thumbnail = MediaObject.objects.filter(media_type="VIDEO")
        else:
            media_needing_thumbnail = MediaObject.objects.filter(
                media_type="VIDEO", thumbnail_image__isnull=True
            )
        print(
            f"Scheduling thumbnail generation for {len(media_needing_thumbnail)} media objects."
        )
        if len(media_needing_thumbnail) == 0:
            print(
                "All thumbnailable media objects already have thumbnails. Pass --all to re-thumbnail all media."
            )
        for media_object in media_needing_thumbnail:
            thumbnail_video.enqueue(media_object.pk)
            if options["verbose"]:
                print(f"Scheduled thumbnail processing for media {media_object}.")
