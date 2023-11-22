from turbo_response import TurboStream
from apps.channel.models import Video


def like(self, video, user):
    try:
        users_like = video.users_like.all()
        users_dislike = video.users_dislike.all()

        if user in users_like:
            video.users_like.remove(user)
            html = TurboStream(f"like--action").update.template("components/blocks/thumbs/_like.html",
                                                                {'video': video}).render()
        else:
            video.users_like.add(user)
            if user in users_dislike:
                video.users_dislike.remove(user)
            html = TurboStream(f"like--action").update.template("components/blocks/thumbs/_liked.html",
                                                                {'video': video}).render()

        self.send(text_data=html)

    except Video.DoesNotExist:
        pass


def dislike(self, video, user):
    try:
        users_dislike = video.users_dislike.all()
        users_like = video.users_like.all()

        if user in users_dislike:
            video.users_dislike.remove(user)
            html = TurboStream(f"yt-video-{video.uid}-like--action").update.template(
                "components/blocks/thumbs/_like.html", {'video': video}).render()
        else:
            video.users_dislike.add(user)
            if user in users_like:
                video.users_like.remove(user)
            html = TurboStream(f"yt-video-{video.uid}-like--action").update.template(
                "components/blocks/thumbs/_disliked.html", {'video': video}).render()

        self.send(text_data=html)
    except Video.DoesNotExist:
        pass
