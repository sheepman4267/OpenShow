import pathlib, subprocess, json

from django.conf import settings
from django.utils.text import slugify

from slides.models import MediaObject
from ffmpeg import FFmpeg, Progress
import hashlib

def get_file_hash(file):
    hash_func = hashlib.new('sha256')
    with open(file, 'rb') as file:
        while chunk := file.read(65536):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_mediafile_seconds(media_path):
    result = subprocess.check_output(
        f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{settings.MEDIA_ROOT + media_path}"',
        shell=True).decode()
    fields = json.loads(result)['streams'][0]

    duration = fields['tags']['DURATION']
    # fps = eval(fields['r_frame_rate'])
    return duration

def transcode_video(media_object_pk: int) -> None:
    media_object = MediaObject.objects.get(pk=media_object_pk)
    final_file_name = slugify(media_object.title) + '.mp4'
    tmp_transcode_out_path = settings.MEDIA_ROOT + '/media_final/video/' + final_file_name
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
    media_object.file_hash = get_file_hash(media_object.final_file.path)
    media_object.save()


def transcode_audio(media_object_pk: int) -> None:
    media_object = MediaObject.objects.get(pk=media_object_pk)
    final_file_name = slugify(media_object.title) + '.mp3'
    tmp_transcode_out_path = settings.MEDIA_ROOT + '/media_final/audio/' + final_file_name
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
    media_object.file_hash = get_file_hash(media_object.final_file.path)
    media_object.save()