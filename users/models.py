from django.db import models
from django.contrib.auth.models import User
from users.choices import USER_TYPES

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	user_type = models.IntegerField(choices = USER_TYPES, default = 0)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    instance.profile.save()

