from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Project
from .models import MentorshipRequest, Profile


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role = user.profile.role

            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'alumni':
                return redirect('alumni_dashboard')
            elif role == 'faculty':
                return redirect('faculty_dashboard')

    return render(request, 'login.html')



@login_required
def student_dashboard(request):
    # only alumni users
    alumni_profiles = Profile.objects.filter(role='alumni')

    # optional filter (by username for now)
    search = request.GET.get('search')
    if search:
        alumni_profiles = alumni_profiles.filter(user__username__icontains=search)

    return render(request, 'student_dashboard.html', {
        'alumni_profiles': alumni_profiles
    })



@login_required
def alumni_dashboard(request):
    # show requests sent TO this alumni
    requests = MentorshipRequest.objects.filter(
        alumni=request.user
    )

    return render(request, 'alumni_dashboard.html', {
        'requests': requests
    })


@login_required
def accept_mentorship_request(request, request_id):
    mentorship_request = MentorshipRequest.objects.get(id=request_id)

    # only alumni can accept their own requests
    if mentorship_request.alumni == request.user:
        mentorship_request.status = 'accepted'
        mentorship_request.save()

    return redirect('alumni_dashboard')


@login_required
def faculty_dashboard(request):
    return render(request, 'faculty_dashboard.html')



@login_required
def create_project(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']

        Project.objects.create(
            title=title,
            description=description,
            faculty=request.user
        )
        return redirect('faculty_dashboard')

    return render(request, 'create_project.html')

@login_required
def send_mentorship_request(request, alumni_id):
    alumni_user = User.objects.get(id=alumni_id)

    MentorshipRequest.objects.get_or_create(
        student=request.user,
        alumni=alumni_user
    )

    return redirect('student_dashboard')

from .models import Project

@login_required
def student_projects(request):
    projects = Project.objects.all()
    return render(request, 'student_projects.html', {
        'projects': projects
    })

@login_required
def join_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.students.add(request.user)
    return redirect('student_projects')

from .models import Project
from django.contrib.auth.decorators import login_required 

@login_required
def faculty_projects(request):
    projects = Project.objects.filter(faculty=request.user)
    return render(request, 'faculty_projects.html', {
        'projects': projects
    })