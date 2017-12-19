from django.db import models
from django.contrib.auth.models import User
from users.choices import USER_TYPES, REVIEW_STATUS, STATUS

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

class Document(models.Model):
	docfile = models.FileField(upload_to='submissions/')

class UserSubmissions(models.Model):
	profile = models.OneToOneField(Profile, on_delete = models.CASCADE)
	submission = models.OneToOneField(Document, on_delete = models.CASCADE)
	submitted_at = models.DateTimeField(auto_now_add = True)
	status = models.IntegerField(choices = REVIEW_STATUS, default = -1)

class SubmissionsReviewer(models.Model):
	submission = models.OneToOneField(UserSubmissions, on_delete = models.CASCADE)
	reviewer = models.OneToOneField(Profile, on_delete = models.CASCADE)
	status = models.IntegerField(choices = STATUS, default = 0)
