from turbo_response import TurboStream
from django.apps import apps
from django.shortcuts import get_object_or_404

from apps.channel.models import Reply


def display_reply_form(self, data):
    obj_id = data.get('id')
    model_name = data.get('model_name')
    model = apps.get_model('channel', model_name)
    obj = get_object_or_404(model, id=obj_id)

    match model_name:
        case 'reply':
            html = TurboStream(
                f"video-{obj.reference.video.uid}-comment-{obj.id}-reply-content").append \
                .template("components/blocks/comments/_reply_form.html", {'object': obj}).render()
            self.send(text_data=html)

        case 'comment':
            html = TurboStream(f"video-{obj.video.uid}-comment-{obj.id}-content").append.template(
                "components/blocks/comments/_reply_form.html", {
                    'object': obj,
                }).render()
            self.send(text_data=html)


def close_reply_form(self, data):
    comment_id = data.get('id')
    model_name = data.get('model_name')
    model = apps.get_model('channel', model_name)
    comment = get_object_or_404(model, id=comment_id)

    match model_name:
        case 'reply':
            if comment.reference.get_model_name() == 'comment':
                html = TurboStream(
                    f"video-{comment.reference.video.uid}-comment-{comment.id}-reply-form").remove.render()
            else:
                html = TurboStream(
                    f"video-{comment.reference.reference.video.uid}-comment-{comment.id}-reply-form").remove.render()
            self.send(text_data=html)
        case 'comment':
            html = TurboStream(f"video-{comment.video.uid}-comment-{comment.id}-reply-form").remove.render()
            self.send(text_data=html)


def reply_comment(self, data, user):
    model_name = data.get('model_name')
    reply_content = data.get('content')
    comment_id = data.get('comment_id')
    model = apps.get_model('channel', model_name)

    if reply_content and comment_id:
        comment = model.objects.get(id=comment_id)

        match model_name:
            case 'reply':
                reply = Reply.objects.create(user=user, reference=comment.reference, content=reply_content,
                                             reply_to=comment)
                html = TurboStream(
                    f"video-{comment.reference.video.uid}-comment-{comment.reference.id}-replies").append.template(
                    "components/blocks/comments/items/_reply_item.html", {
                        "reply": reply,
                        "user": user
                    }).render()
                self.send(text_data=html)

            case 'comment':
                reply = Reply.objects.create(user=user, reference=comment, content=reply_content)
                html = TurboStream(
                    f"video-{comment.video.uid}-comment-{comment.id}-replies").append.template(
                    "components/blocks/comments/items/_reply_item.html", {
                        "reply": reply,
                        "user": user
                    }).render()
                self.send(text_data=html)
