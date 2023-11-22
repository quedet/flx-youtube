from moviepy.editor import VideoFileClip
from django.template import Library
from time import strftime, gmtime

register = Library()


@register.filter
def get_video_duration(value):
    video = VideoFileClip(value.source.path)
    duration = gmtime(video.duration)
    if duration.tm_hour > 0:
        return strftime("%H:%M:%S", duration)
    return strftime("%M:%S", duration)


@register.filter
def get_model_name(value):
    if value._meta.model_name == 'videodraft':
        return 'Draft'
    return 'Published'