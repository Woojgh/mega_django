from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings
from helpers.s3 import upload_image_with_custom_uuid
from discord_bind.models import DiscordUser


class UserProfile(models.Model):
    """Model of user profile."""


    UPLOAD_TO = 'profile_photos'
    uuid_photo = models.UUIDField(default=uuid.uuid4, editable=False)
    uuid_cover = models.UUIDField(default=uuid.uuid4, editable=False)

    # Auth User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # User details
    photo = models.ImageField(
        upload_to=upload_image_with_custom_uuid('uuid_photo'),
        null=True, blank=True, verbose_name=_('photo'), max_length=255,
    )
    cover_photo = models.ImageField(
        upload_to=upload_image_with_custom_uuid('uuid_cover'),
        null=True, blank=True,verbose_name=_('photo'), max_length=255,
    )
    phone_number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('phone number'),
    )
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('address'),
    )
    zip_code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_('zip code'),
    )
    city = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('city'),
    )
    state = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_('state'),
    )
    country = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_('country'),
    )
    

    def __str__(self):
        """."""

        return '{} ({})'.format(self.user.email, self.account_type)

    def save(self, *args, **kwargs):
        """Create a profile on Fatsecret in addition to locally."""
        if not self.id:
            self.fat_oauth_token, self.fat_oauth_secret = fs_api.profile_create()
        super(UserProfile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_discord_user(sender, **kwargs):
    # d_account = DiscordUser(
    #     user=kwargs['instance']
    # )

    # d_account.save()
    dis_user, created = DiscordUser.objects.get_or_create(user=kwargs['instance'], uid=kwargs['instance'].id)

