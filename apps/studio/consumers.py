import re

from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from pprint import pprint
from django.shortcuts import get_object_or_404
from turbo_response import TurboStream

from apps.channel.models import Video, Playlist, Topic, Channel, ChannelLink

from django.apps import apps
from guardian.shortcuts import ObjectPermissionChecker


class StudioConsumer(JsonWebsocketConsumer):
    channel_uid = None

    def connect(self):
        """"""
        self.accept()
        self.channel_uid = self.scope['url_route']['kwargs']['group_name']

        async_to_sync(self.channel_layer.group_add)(self.channel_uid, self.channel_name)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.channel_uid, self.channel_name)

    def send_response(self, content):
        html = content['html']

        self.send_json({
            'type': 'send response',
            'html': html
        })

    def receive_json(self, content, **kwargs):
        data = content.get('data')
        user = self.scope['user']
        video = None
        topic = None
        model = None

        if 'model_name' in data:
            model_name = data.get('model_name')
            app_label = None

            if model_name == 'video':
                app_label = 'channel'
            elif model_name == 'videodraft':
                app_label = 'studio'

            model = apps.get_model(app_label=app_label, model_name=model_name)

        if 'video_id' in data:
            video = get_object_or_404(model, id=data.get('video_id'), author=user)

        if 'topic_id' in data:
            topic = get_object_or_404(Topic, id=data.get('topic_id'))

        match content['action']:
            case 'set video topic':
                if topic not in video.topics.all():
                    video.topics.add(topic)
                    html = TurboStream(f"yt--topic--{topic.id}").remove.render()
                    self.send(text_data=html)

            case 'set topic to selected list':
                if topic in video.topics.all():
                    html = TurboStream("yt--topics--selected").append.template(
                        "pages/studio/video/topics/selected.html", {'topic': topic, 'video': video}).render()
                    self.send(html)

            case 'set topic to video form':
                if topic in video.topics.all():
                    context = {
                        'topic': topic
                    }
                    if video.topics.count() > 1:
                        context.update({
                            'first': False
                        })
                    else:
                        context.update({
                            'first': True
                        })

                    html = TurboStream("yt-video-selected-topics").append.template(
                        "pages/studio/video/topics/item.html", context).render()
                    self.send(html)

            case 'remove topic to video form':
                if topic not in video.topics.all():
                    html = TurboStream(f"yt-video-topic-{topic.id}").remove.render()
                    self.send(html)

            case 'remove video topic':
                if topic in video.topics.all():
                    video.topics.remove(topic)
                    html = TurboStream(f"yt--topic--{topic.id}--item").remove.render()
                    self.send(text_data=html)

            case 'delete playlist':
                playlist_id = data.get('playlist_id')
                playlist = get_object_or_404(Playlist, id=playlist_id, channel__author=user)
                playlist.delete()
                html = TurboStream(f"yt--playlist--{playlist_id}").remove.render()
                self.send(text_data=html)

            case 'upload video':
                pprint(content['data'])

            case 'content changed':
                data = content['data']
                video_id = data['id']
                video = get_object_or_404(Video, id=video_id)

                changed = False

                if video.title != data['title']:
                    changed = True

                if video.description != data['description']:
                    changed = True

                if video.playlist and video.playlist.id != data['playlist']:
                    changed = True

                if video.playlist is None and data['playlist']:
                    changed = True

                if data.get('thumbnail') is not None:
                    changed = True

                if changed:
                    html = TurboStream("VideoEditionSubmitButton").update.\
                        template("pages/studio/details/_button_enabled.html").render()
                else:
                    html = TurboStream("VideoEditionSubmitButton").update.\
                        template("pages/studio/details/_button_disabled.html").render()

                self.send(text_data=html)

            case 'show link form':
                channel_id = data.get('channel_id')
                html = TurboStream('yt-channel-links').append.template('pages/studio/customization/basic/links/form.html', {
                    'channel_id': channel_id
                }).render()
                self.send(text_data=html)

            case 'add link':
                channel_id = data.get('channel_id')
                title = data.get('title', None)
                url = data.get('url', None)

                channel = get_object_or_404(Channel, id=channel_id)
                checker = ObjectPermissionChecker(user)

                if checker.has_perm('change_channel', channel):
                    if title and re.match('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', url):
                        link = ChannelLink.objects.create(channel_id=channel_id, title=title, url=url)

                        html = TurboStream('yt-channel-links').append.template('pages/studio/customization/basic/links/item.html', {
                            'link': link
                        }).render()
                    else:
                        html = TurboStream('yt-channel-links').append.template('pages/studio/customization/basic/links/form.html', {
                            'title': title,
                            'url': url,
                            'error': 'error'
                        }).render()

                    self.send(text_data=html)
