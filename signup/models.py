from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .form import SignUpForm as s
# Create your models here.
class Profile(models.Model):


	user = models.OneToOneField(User,on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100, blank=True)
	bio = models.TextField(max_length=500,blank=True)
	location = models.CharField(max_length=30,blank=True)
	birthdate = models.DateField(null=True,blank=True)

	class Meta:
		db_table = "signup_profile"

	def __str__(self):
		return self.first_name


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()