from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Every User gets a matching Profile the moment their account exists."""
    if created:
        Profile.objects.create(user=instance)
    else:
        # Profile might not exist yet for users created before this
        # signal existed (e.g. via the shell) — create it defensively.
        Profile.objects.get_or_create(user=instance)
