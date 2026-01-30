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

    # 🔹 COMMON PERSONAL INFO
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    address = models.TextField(blank=True)
    # profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    college_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year_of_study = models.IntegerField(null=True,blank=True)

    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return f"Student - {self.profile.user.username}"
    

class AlumniProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=200)
    current_role = models.CharField(max_length=150)
    domain = models.CharField(max_length=100)
    experience_years = models.IntegerField(null=True)

    bio = models.TextField(blank=True)
    expertise = models.TextField(blank=True)

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    available_for_mentorship = models.BooleanField(default=True)

    def __str__(self):
        return f"Alumni - {self.profile.user.username}"
    

class FacultyProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=150)

    expertise = models.TextField(blank=True)
    research_interests = models.TextField(blank=True)

    official_email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return f"Faculty - {self.profile.user.username}"

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
