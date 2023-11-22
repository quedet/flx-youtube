from channels.generic.websocket import JsonWebsocketConsumer
from apps.channel.models import Video, Comment, Channel, Contact
from apps.accounts.models import User

from django.shortcuts import get_object_or_404

from turbo_response import TurboStream

#
from .actions import (
    reply as reply_actions, comment as comment_actions,
    core as core_actions)


class AssetController(JsonWebsocketConsumer):
    def connect(self):
        """Event when client connects"""
        self.accept()

    def receive_json(self, content, **kwargs):
        data = content.get('data')
        action = content['action']
        user = self.scope['user']
        video = None

        if data.get('video_uid'):
            video = get_object_or_404(Video, uid=data.get('video_uid'))

        match action:
            case 'like video':
                core_actions.like(self, key=data.get('video_uid'), user=user, app_label='channel', model_name='video')

            case 'dislike video':
                core_actions.dislike(self, key=data.get('video_uid'), user=user, app_label='channel', model_name='video')

            case 'like comment':
                model_name = data.get('model_name')
                core_actions.like(self, key=data.get('id'), user=user, app_label='channel', model_name=model_name)

            case 'dislike comment':
                model_name = data.get('model_name')
                core_actions.dislike(self, key=data.get('id'), user=user, app_label='channel', model_name=model_name)

            # Comment Layout
            case "display comment form":
                comment_actions.display_comment_creation_form(self, video=video)

            case "close comment form":
                comment_actions.close_comment_creation_form(self, video=video)

            # Comment Creation
            case "comment video":
                comment_actions.comment_video(self, data=data, user=user, video=video)

            # Comment Edition
            case "display comment edition form":
                comment_actions.display_comment_edition_form(self, data=data, user=user)

            case "close comment edition form":
                comment_actions.close_comment_edition_form(self, data=data, user=user)

            case "edit comment":
                comment_actions.edit_comment(self, data=data, user=user)

            # Comment Deletion
            case "delete comment":
                comment_actions.delete_comment(self, data=data, user=user)

            # Reply Layout
            case "display comment reply form":
                reply_actions.display_reply_form(self, data=data)

            case "close comment reply form":
                reply_actions.close_reply_form(self, data=data)

            case "reply comment":
                reply_actions.reply_comment(self, data=data, user=user)

            # Preview
            case "start preview":
                core_actions.startPreview(self, video)
            case "stop preview":
                core_actions.stopPreview(self, video)

            # Filters
            case "filter by newest first":
                comments = Comment.objects.filter(video=video).order_by('-created')
                html = TurboStream(f"yt--video-{ video.uid }-comments").update.template(
                    "components/blocks/comments/lists/_comments_list.html", {"comments": comments, "user": user}).render()
                self.send(text_data=html)

            case "filter by top comments":
                comments = Comment.objects.filter(video=video).order_by('-total_likes')
                html = TurboStream(f"yt--video-{video.uid}-comments").update.template(
                    "components/blocks/comments/lists/_comments_list.html", {"comments": comments, "user": user}).render()
                self.send(text_data=html)

            case 'filter by topics':
                data = content['data']
                if data['topic'] == 'all':
                    videos = Video.objects.all()
                else:
                    videos = Video.objects.filter(topics__slug=data['topic'])

                html = TurboStream(f"videos--list").update.template(
                    "components/blocks/videos/_lists.html", {
                        "videos": videos
                    }).render()
                self.send(text_data=html)

            # Following System
            case 'follow channel':
                data = content['data']
                channel_id = data['channel_id']
                channel = get_object_or_404(Channel, id=channel_id)

                contact, created = Contact.objects.get_or_create(user_from=user, user_to=channel)

                if not created:
                    Contact.objects.filter(user_from=user, user_to=channel).delete()
                    html = TurboStream("subscribe--action").update.template("components/blocks/thumbs/_subscribe.html", {
                        'channel': channel
                    }).render()
                else:
                    html = TurboStream("subscribe--action").update.template("components/blocks/thumbs/_subscribed.html", {
                        'channel': channel
                    }).render()

                self.send(text_data=html)