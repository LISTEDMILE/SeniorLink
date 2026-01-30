from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile, StudentProfile, AlumniProfile, FacultyProfile


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        # create base profile
        profile = Profile.objects.create(
            user=instance,
            role='student',      # default role (we update later)
            full_name=instance.username
        )

        # create role-specific profiles
        StudentProfile.objects.create(profile=profile)
        AlumniProfile.objects.create(profile=profile)
        FacultyProfile.objects.create(profile=profile)