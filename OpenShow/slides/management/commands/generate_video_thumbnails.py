from django.core.management.base import BaseCommand, CommandError
from slides.models import MediaObject
from django_q.models import Schedule
from datetime import datetime, UTC


class Command(BaseCommand):
    help = "Schedules MediaObjects with media type \"Video\" and no thumbnail image for thumbnail processing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Schedule all videos for thumbnail processing (e.g. to reflect a change to how thumbnails are generated)"
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Verbose output"
        )

    def handle(self, *args, **options):
        if options["all"]:
            media_needing_thumbnail = MediaObject.objects.filter(media_type="VIDEO")
        else:
            media_needing_thumbnail = MediaObject.objects.filter(media_type="VIDEO", thumbnail_image__isnull=True)
        print(f'Scheduling thumbnail generation for {len(media_needing_thumbnail)} media objects.')
        if len(media_needing_thumbnail) == 0:
            print(f'All thumbnailable media objects already have thumbnails. Pass --all to re-thumbnail all media.')
        for media_object in media_needing_thumbnail:
            Schedule.objects.create(
                func='slides.editor.tasks.thumbnail_video',
                args=media_object.pk,
                schedule_type=Schedule.ONCE,
                next_run=datetime.now(UTC),
            )
            if options["verbose"]:
                print(f'Scheduled thumbnail processing for media {media_object}.')
