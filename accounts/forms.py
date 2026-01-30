from django import forms
from .models import StudentProfile, AlumniProfile, FacultyProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            # ===== BASIC INFO =====
            'college_name',
            'degree',
            'branch',
            'year_of_study',

            # ===== SKILLS & INTERESTS =====
            'skills',
            'interests',

            # ===== SOCIAL LINKS =====
            'github',
            'linkedin',

            # ===== CURRENT PROJECT =====
            'current_project_title',
            'current_project_domain',
            'current_project_description',
            'current_project_technologies',
            'current_project_role',
            'current_project_status',
            'current_project_start_date',
            'current_project_progress',
        ]

        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 3}),
            'current_project_description': forms.Textarea(attrs={'rows': 4}),
            'current_project_technologies': forms.TextInput(
                attrs={'placeholder': 'React, Django, PostgreSQL'}
            ),
            'current_project_progress': forms.NumberInput(
                attrs={'min': 0, 'max': 100}
            ),
            'current_project_start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }



class AlumniProfileForm(forms.ModelForm):
    interested_domains = forms.CharField(
        required=False,
        help_text="Enter domains separated by commas (e.g. AI, Web, Cloud)"
    )

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
            'interested_domains',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 Convert list → string for display
        if self.instance and isinstance(self.instance.interested_domains, list):
            self.initial['interested_domains'] = ", ".join(
                self.instance.interested_domains
            )

    def clean_interested_domains(self):
        data = self.cleaned_data.get('interested_domains', '')
        if not data:
            return []
        return [d.strip() for d in data.split(',') if d.strip()]




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

        widgets = {
            'expertise': forms.Textarea(attrs={'rows': 3}),
            'research_interests': forms.Textarea(attrs={'rows': 3}),
        }
