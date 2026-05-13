from django.db.models.signals import post_save
from django.dispatch import receiver

from authApp.models import CustomUser

from .models import UserDetails, build_public_slug


@receiver(post_save, sender=CustomUser)
def refresh_user_details_public_slug(sender, instance, **kwargs):
    """Keep URL slug in sync when the display username changes."""
    try:
        details = instance.details
    except UserDetails.DoesNotExist:
        return
    desired = build_public_slug(instance.username, details.pk)
    if details._slug != desired:
        UserDetails.objects.filter(pk=details.pk).update(_slug=desired)
