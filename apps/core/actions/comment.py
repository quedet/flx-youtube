from turbo_response import TurboStream
from django.apps import apps
from django.shortcuts import get_object_or_404

from guardian.core import ObjectPermissionChecker

from apps.channel.models import Comment


# Creation
def display_comment_creation_form(self, video):
    html = TurboStream("comment-form-renderer").update.template("components/blocks/comments/_form_renderer.html", {
        'video': video
    }).render()
    self.send(text_data=html)


def close_comment_creation_form(self, video):
    html = TurboStream("comment-form-renderer").update.template("components/blocks/comments/_form_placeholder.html", {
        'video': video
    }).render()

    self.send(text_data=html)


def comment_video(self, data, user, video):
    comment_content = data.get('content')

    if comment_content:
        new_comment = Comment.objects.create(user=user, video=video, content=comment_content)

        html = TurboStream(f"yt--video-{video.uid}-comments").append.template(
            "components/blocks/comments/items/_comment_item.html", {"comment": new_comment, "user": user}).render()

        self.send(text_data=html)


# Removal
def delete_comment(self, data, user):
    model_name = data.get('model_name')
    model = apps.get_model('channel', model_name)
    obj_id = data.get('id')
    obj = get_object_or_404(model, id=obj_id, user=user)
    checker = ObjectPermissionChecker(user)

    if checker.has_perm(f'delete_{obj.get_model_name()}', obj):
        if obj.get_model_name() == 'reply':
            obj_video_uid = obj.reference.video.uid
            html = TurboStream(f"video-{obj_video_uid}-comment-{obj_id}-reply").remove.render()
        else:
            obj_video_uid = obj.video.uid
            html = TurboStream(f"video-{obj_video_uid}-comment-{obj_id}").remove.render()

        obj.delete()
        self.send(text_data=html)
    else:
        print("Sorry no permission granted for this object.")


# Edition
def display_comment_edition_form(self, data, user):
    model_name = data.get('model_name')
    model = apps.get_model('channel', model_name)
    obj_id = data.get('id')
    obj = get_object_or_404(model, id=obj_id, user=user)
    checker = ObjectPermissionChecker(user)
    print(obj)

    if checker.has_perm(f'change_{obj.get_model_name()}', obj):
        if obj.get_model_name() == 'reply':
            html = TurboStream(f"video-{obj.reference.video.uid}-comment-{obj.id}-reply-content").update.template(
                "components/blocks/comments/_reply_edit_form.html", {'reply': obj}).render()
        else:
            html = TurboStream(f"video-{obj.video.uid}-comment-{obj.id}-content").update.template(
                "components/blocks/comments/_comment_form.html", {'comment': obj}).render()

        self.send(text_data=html)


def close_comment_edition_form(self, data, user):
    model_name = data.get('model_name')
    model = apps.get_model('channel', model_name)
    obj_id = data.get('id')
    obj = get_object_or_404(model, id=obj_id, user=user)

    if model_name == 'reply':
        if obj.reference:
            html = TurboStream(f"video-{obj.reference.video.uid}-comment-{obj.id}-content").update.template(
                "components/blocks/comments/items/_reply_item_content.html", {'reply': obj, 'user': user}).render()
        else:
            html = TurboStream(f"video-{obj.video.uid}-comment-{obj.id}-content").update.template(
                "components/blocks/comments/items/_reply_item_content.html", {'reply': obj, 'user': user}).render()
    else:
        html = TurboStream(f"video-{obj.video.uid}-comment-{obj.id}-content").update.template(
            "components/blocks/comments/items/_comment_item_content.html", {'comment': obj, 'user': user}).render()
    self.send(text_data=html)


def edit_comment(self, data, user):
    model_name = data.get('model_name')
    model = apps.get_model('channel', model_name)
    obj_id = data.get('id')
    obj_content = data.get('content')
    obj = get_object_or_404(model, id=obj_id, user=user)

    checker = ObjectPermissionChecker(user)

    if checker.has_perm(f'change_{obj.get_model_name()}', obj):
        if obj_content and obj_content != obj.content:
            obj.content = obj_content
            obj.save()

        if obj.get_model_name() == 'reply':
            html = TurboStream(f"video-{obj.reference.video.uid}-comment-{obj.id}-reply-content").update.template(
                "components/blocks/comments/items/_reply_item_content.html",
                {'reply': obj, 'user': user}).render()
        else:
            html = TurboStream(f"video-{obj.video.uid}-comment-{obj.id}-content").update.template(
                "components/blocks/comments/items/_comment_item_content.html", {'comment': obj, 'user': user}) \
                .render()

        self.send(text_data=html)
    else:
        print("Sorry no permission granted for this object.")
