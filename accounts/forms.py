from django import forms
from .models import StudentProfile, AlumniProfile, FacultyProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'college_name',
            'degree',
            'branch',
            'year_of_study',
            'skills',
            'interests',
            'github',
            'linkedin',
        ]


class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = [
            'company_name',
            'current_role',
            'domain',
            'experience_years',
            'bio',
            'expertise',
            'linkedin',
            'github',
            'available_for_mentorship',
        ]


class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = [
            'department',
            'designation',
            'qualification',
            'expertise',
            'research_interests',
            'official_email',
            'linkedin',
        ]