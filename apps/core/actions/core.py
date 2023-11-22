from django.apps import apps
from turbo_response import TurboStream
from django.shortcuts import get_object_or_404
import redis

from django.conf import settings
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def like(self, key, user, app_label, model_name):
    model = apps.get_model(app_label=app_label, model_name=model_name)

    if model_name == 'video':
        obj = get_object_or_404(model, uid=key)
    else:
        obj = get_object_or_404(model, id=key)

    users_like = obj.users_like.all()
    users_dislike = obj.users_dislike.all()

    if user in users_like:
        obj.users_like.remove(user)

        if model_name == 'video':
            html = TurboStream(f"yt-{model_name}-{obj.uid}-like--action").update.template(
                "components/blocks/thumbs/_like.html", {str(model_name): obj}).render()
        else:
            html = TurboStream(f"yt-{model_name}-{obj.id}-like--action").update.template(
                "components/blocks/comments/thumbs/_like.html", {'obj': obj}).render()
    else:
        obj.users_like.add(user)

        if user in users_dislike:
            obj.users_dislike.remove(user)

        if model_name == 'video':
            html = TurboStream(f"yt-{model_name}-{obj.uid}-like--action").update.template(
                "components/blocks/thumbs/_liked.html", {str(model_name): obj}).render()
        else:
            html = TurboStream(f"yt-{model_name}-{obj.id}-like--action").update.template(
                "components/blocks/comments/thumbs/_liked.html", {'obj': obj}).render()

    self.send(text_data=html)


def dislike(self, key, user, app_label, model_name):
    model = apps.get_model(app_label=app_label, model_name=model_name)

    if model_name == 'video':
        obj = get_object_or_404(model, uid=key)
    else:
        obj = get_object_or_404(model, id=key)

    users_dislike = obj.users_dislike.all()
    users_like = obj.users_like.all()

    if user in users_dislike:
        obj.users_dislike.remove(user)

        if model_name == 'video':
            html = TurboStream(f"yt-{model_name}-{obj.uid}-like--action").update.template(
                "components/blocks/thumbs/_like.html", {str(model_name): obj}).render()
        else:
            html = TurboStream(f"yt-{model_name}-{obj.id}-like--action").update.template(
                "components/blocks/comments/thumbs/_like.html", {'obj': obj}).render()
    else:
        obj.users_dislike.add(user)

        if user in users_like:
            obj.users_like.remove(user)

        if model_name == 'video':
            html = TurboStream(f"yt-{model_name}-{obj.uid}-like--action").update.template(
                "components/blocks/thumbs/_disliked.html", {str(model_name): obj}).render()
        else:
            html = TurboStream(f"yt-{model_name}-{obj.id}-like--action").update.template(
                "components/blocks/comments/thumbs/_disliked.html", {'obj': obj}).render()

    self.send(text_data=html)


def startPreview(self, video):
    # increment total video views by 1
    r.incr(f'video:{video.id}:views')
    # increment video ranking by 1
    r.zincrby(f'video_ranking', 1, video.id)

    html = TurboStream(f"yt--video--{video.uid}").update.template("components/blocks/videos/_preview.html", {"video": video}).render()
    self.send(text_data=html)


def stopPreview(self, video):
    html = TurboStream(f"yt--video--{video.uid}").update.template("components/blocks/videos/_thumbnail.html", {"video": video}).render()
    self.send(text_data=html)