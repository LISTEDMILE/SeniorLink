from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Project, MentorshipRequest, Profile,
    StudentProfile, AlumniProfile, FacultyProfile
)
from .forms import StudentProfileForm, AlumniProfileForm, FacultyProfileForm
from .decorators import role_required


def home(request):
    return render(request, 'home.html')



def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.profile.role = role
        user.profile.save()

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            role_redirects = {
                "student": "student_dashboard",
                "alumni": "alumni_dashboard",
                "faculty": "faculty_projects",  # 👈 special case
            }

            return redirect(role_redirects.get(user.profile.role))

        messages.error(request, "Invalid credentials")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@role_required('student')
def student_dashboard(request):
    alumni_profiles = Profile.objects.filter(role='alumni')

    sent_requests = MentorshipRequest.objects.filter(student=request.user)
    status_map = {r.alumni.id: r.status for r in sent_requests}

    for alumni in alumni_profiles:
        alumni.request_status = status_map.get(alumni.user.id)

    

    return render(request, 'student_dashboard.html', {
        'alumni_profiles': alumni_profiles
    })


@role_required('student')
def student_projects(request):
    return render(request, 'student_projects.html', {
        'projects': Project.objects.all()
    })


@role_required('student')
def send_mentorship_request(request, alumni_id):
    alumni = get_object_or_404(User, id=alumni_id)
    MentorshipRequest.objects.get_or_create(
        student=request.user,
        alumni=alumni
    )
    return redirect('student_dashboard')


@role_required('student')
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.students.add(request.user)
    messages.success(request, "You joined the project successfully")
    return redirect('student_projects')



@role_required('alumni')
def alumni_dashboard(request):
    return render(request, 'alumni_dashboard.html', {
        'requests': MentorshipRequest.objects.filter(alumni=request.user)
    })


@role_required('alumni')
def accept_mentorship_request(request, request_id):
    req = get_object_or_404(MentorshipRequest, id=request_id, alumni=request.user)
    req.status = 'accepted'
    req.save()
    return redirect('alumni_dashboard')

@role_required('alumni')
def decline_mentorship_request(request, request_id):
    req = get_object_or_404(MentorshipRequest, id=request_id, alumni=request.user)
    req.status = 'declined'
    req.save()
    return redirect('alumni_dashboard')


@role_required('alumni')
def alumni_projects(request):
    return render(request, 'alumni_projects.html', {
        'projects': Project.objects.all()
    })


@role_required('alumni')
def join_project_as_alumni(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.alumni.add(request.user)
    messages.success(request, "You are now mentoring this project")
    return redirect('alumni_projects')


@role_required('faculty')
def faculty_dashboard(request):
    return render(request, 'faculty_dashboard.html')


@role_required('faculty')
def create_project(request):
    if request.method == "POST":
        Project.objects.create(
            title=request.POST['title'],
            short_description=request.POST['short_description'],
            description=request.POST['description'],
            domain=request.POST['domain'],
            technologies=request.POST['technologies'],
            difficulty_level=request.POST['difficulty_level'],
            start_date=request.POST['start_date'],
            end_date=request.POST.get('end_date') or None,
            max_students=request.POST['max_students'],
            github_link=request.POST.get('github_link'),
            documentation_link=request.POST.get('documentation_link'),
            status='open',
            faculty=request.user
        )
        messages.success(request, "Project created successfully")
        return redirect('faculty_projects')

    return render(request, 'create_project.html')


@role_required('faculty')
def faculty_projects(request):
    return render(request, 'faculty_projects.html', {
        'projects': Project.objects.filter(faculty=request.user)
    })


@login_required
def edit_profile(request):
    profile = request.user.profile

    model_form_map = {
        'student': (StudentProfile, StudentProfileForm),
        'alumni': (AlumniProfile, AlumniProfileForm),
        'faculty': (FacultyProfile, FacultyProfileForm),
    }

    model, form_class = model_form_map[profile.role]
    instance, _ = model.objects.get_or_create(profile=profile)

    form = form_class(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated")
        return redirect('edit_profile')

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def view_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    context = {
        'profile': profile,
        'student': StudentProfile.objects.filter(profile=profile).first(),
        'alumni': AlumniProfile.objects.filter(profile=profile).first(),
        'faculty': FacultyProfile.objects.filter(profile=profile).first(),
    }

    return render(request, 'view_profile.html', context)
