from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from guardian.shortcuts import assign_perm

from apps.accounts.models import User


@receiver(post_save, sender=User)
def user_post_create(sender, instance, created, **kwargs):
    if created and instance.username is not "AnonymousUser":
        permissions = ['accounts.add_user', 'accounts.change_user', 'accounts.delete_user', 'accounts.view_user']
        for perm in permissions:
            assign_perm(perm, instance, instance)


@receiver(post_delete, sender=User)
def user_post_delete(sender, instance, **kwargs):
    if instance.profile:
        instance.profile.delete(save=False)
