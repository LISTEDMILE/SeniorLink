from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('faculty', 'Faculty'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    faculty = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )
    students = models.ManyToManyField(
        User,
        blank=True,
        related_name='joined_projects'
    )
    alumni = models.ManyToManyField(
        User,
        blank=True,
        related_name='mentored_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class MentorshipRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    alumni = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=20,
        choices=[('pending','Pending'), ('accepted','Accepted')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
 