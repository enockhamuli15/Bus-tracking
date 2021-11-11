from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cash


@receiver(post_save, sender='TapGoApp.Profile')
def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        Cash.objects.create(account=instance)