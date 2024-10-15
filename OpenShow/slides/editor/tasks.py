import pathlib

from django.conf import settings
from django.utils.text import slugify

from slides.models import MediaObject
from ffmpeg import FFmpeg, Progress

def transcode_video(media_object_pk: int) -> None:
    media_object = MediaObject.objects.get(pk=media_object_pk)
    final_file_name = slugify(media_object.title) + '.mp4'
    tmp_transcode_out_path = settings.MEDIA_ROOT + 'media_final/video/' + final_file_name
    pathlib.Path(tmp_transcode_out_path).parents[0].mkdir(parents=True, exist_ok=True)
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(media_object.raw_file.path)
        .output(
            tmp_transcode_out_path,
            {"codec:v": "libsvtav1", "codec:a": "mp3"},
            preset=8,
            crf=40,
        )
    )

    @ffmpeg.on("progress")
    def print_progress(progress: Progress):
        print(progress)
        # TODO: Implement an (optional) Redis/Valkey backend for Eventstream so we can send progress back to the editor

    ffmpeg.execute()
    media_object.final_file = 'media_final/video/' + final_file_name
    media_object.save()


def transcode_audio(media_object_pk: int) -> None:
    media_object = MediaObject.objects.get(pk=media_object_pk)
    final_file_name = slugify(media_object.title) + '.mp3'
    tmp_transcode_out_path = settings.MEDIA_ROOT + 'media_final/audio/' + final_file_name
    pathlib.Path(tmp_transcode_out_path).parents[0].mkdir(parents=True, exist_ok=True)
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(media_object.raw_file.path)
        .output(
            tmp_transcode_out_path,
            {"codec:a": "mp3"},
            preset=8,
            crf=40,
        )
    )

    @ffmpeg.on("progress")
    def print_progress(progress: Progress):
        print(progress)
        # TODO: Implement an (optional) Redis/Valkey backend for Eventstream so we can send progress back to the editor

    ffmpeg.execute()
    media_object.final_file = 'media_final/audio/' + final_file_name
    media_object.save()