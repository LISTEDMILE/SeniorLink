from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project, MentorshipRequest, Profile , StudentProfile, AlumniProfile, FacultyProfile
from .forms import StudentProfileForm, FacultyProfileForm, AlumniProfileForm
from .decorators import role_required

def home(request):
    return render(request,'home.html')

# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        # ✅ prevent duplicate usernames
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)

# profile already created by signal
        user.profile.role = role
        user.profile.save()

        return redirect('login')

    return render(request, 'register.html')

 
# ---------------- LOGIN ----------------
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


# ---------------- STUDENT ----------------
@role_required('student')
def student_dashboard(request):
    alumni_profiles = Profile.objects.filter(role='alumni')

    search = request.GET.get('search')
    if search:
        alumni_profiles = alumni_profiles.filter(
            user__username__icontains=search
        )

    return render(request, 'student_dashboard.html', {
        'alumni_profiles': alumni_profiles
    })


@role_required('student')
def student_projects(request):
    projects = Project.objects.all()
    return render(request, 'student_projects.html', {
        'projects': projects
    })


from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project, MentorshipRequest, Profile , StudentProfile, AlumniProfile, FacultyProfile
from .forms import StudentProfileForm, FacultyProfileForm, AlumniProfileForm
from .decorators import role_required

def home(request):
    return render(request,'home.html')

# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        # ✅ prevent duplicate usernames
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)

# profile already created by signal
        user.profile.role = role
        user.profile.save()

        return redirect('login')

    return render(request, 'register.html')

 
# ---------------- LOGIN ----------------
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


# ---------------- STUDENT ----------------
# @role_required('student')
# def student_dashboard(request):
#     alumni_profiles = Profile.objects.filter(role='alumni')

#     search = request.GET.get('search')
#     if search:
#         alumni_profiles = alumni_profiles.filter(
#             user__username__icontains=search
#         )

#     return render(request, 'student_dashboard.html', {
#         'alumni_profiles': alumni_profiles
#     })
@login_required
def student_dashboard(request):
    alumni_profiles = Profile.objects.filter(role='alumni')

    sent_requests = MentorshipRequest.objects.filter(student=request.user)

    status_map = {
        req.alumni.id: req.status
        for req in sent_requests
    }

    for alumni in alumni_profiles:
        alumni.request_status = status_map.get(alumni.user.id)

    return render(request, 'student_dashboard.html', {
        'alumni_profiles': alumni_profiles
    })



@role_required('student')
def student_projects(request):
    projects = Project.objects.all()
    return render(request, 'student_projects.html', {
        'projects': projects
    })


@role_required('student')
def join_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.students.add(request.user)
    return redirect('student_projects')


@role_required('student')
def send_mentorship_request(request, alumni_id):
    alumni_user = User.objects.get(id=alumni_id)

    MentorshipRequest.objects.get_or_create(
        student=request.user,
        alumni=alumni_user
    )

    return redirect('student_dashboard')


# ---------------- ALUMNI ----------------
@role_required('alumni')
def alumni_dashboard(request):
    requests = MentorshipRequest.objects.filter(
        alumni=request.user
    )

    return render(request, 'alumni_dashboard.html', {
        'requests': requests
    })


@role_required('alumni')
def accept_mentorship_request(request, request_id):
    mentorship_request = MentorshipRequest.objects.get(id=request_id)

    if mentorship_request.alumni == request.user:
        mentorship_request.status = 'accepted'
        mentorship_request.save()

    return redirect('alumni_dashboard')


# ---------------- FACULTY ----------------
@role_required('faculty')
def faculty_dashboard(request):
    return render(request, 'faculty_dashboard.html')


@role_required('faculty')
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


@role_required('faculty')
def faculty_projects(request):
    projects = Project.objects.filter(faculty=request.user)
    return render(request, 'faculty_projects.html', {
        'projects': projects
    })


# ---------------- LOGOUT ----------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    profile = request.user.profile

    # STUDENT
    if profile.role == 'student':
        instance, created = StudentProfile.objects.get_or_create(
            profile=profile
        )
        form_class = StudentProfileForm

    # ALUMNI
    elif profile.role == 'alumni':
        instance, created = AlumniProfile.objects.get_or_create(
            profile=profile
        )
        form_class = AlumniProfileForm

    # FACULTY
    else:
        instance, created = FacultyProfile.objects.get_or_create(
            profile=profile
        )
        form_class = FacultyProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = form_class(instance=instance)

    return render(request, 'edit_profile.html', {
        'form': form
    })


@login_required
def view_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    student = None
    alumni = None
    faculty = None

    if profile.role == 'student':
        student = StudentProfile.objects.filter(profile=profile).first()

    elif profile.role == 'alumni':
        alumni = AlumniProfile.objects.filter(profile=profile).first()

    elif profile.role == 'faculty':
        faculty = FacultyProfile.objects.filter(profile=profile).first()

    return render(request, 'view_profile.html', {
        'profile': profile,
        'student': student,
        'alumni': alumni,
        'faculty': faculty,
    })


@role_required('student')
def send_mentorship_request(request, alumni_id):
    alumni_user = User.objects.get(id=alumni_id)

    MentorshipRequest.objects.get_or_create(
        student=request.user,
        alumni=alumni_user
    )

    return redirect('student_dashboard')


# ---------------- ALUMNI ----------------
@role_required('alumni')
def alumni_dashboard(request):
    requests = MentorshipRequest.objects.filter(
        alumni=request.user
    )

    return render(request, 'alumni_dashboard.html', {
        'requests': requests
    })


@role_required('alumni')
def accept_mentorship_request(request, request_id):
    mentorship_request = MentorshipRequest.objects.get(id=request_id)

    if mentorship_request.alumni == request.user:
        mentorship_request.status = 'accepted'
        mentorship_request.save()

    return redirect('alumni_dashboard')




@login_required
def alumni_projects(request):
    # allow only alumni
    if request.user.profile.role != 'alumni':
        return redirect('login')

    projects = Project.objects.all()
    return render(request, 'alumni_projects.html', {
        'projects': projects
    })


@login_required
def join_project_as_alumni(request, project_id):
    if request.user.profile.role != 'alumni':
        return redirect('login')

    project = get_object_or_404(Project, id=project_id)
    project.alumni.add(request.user)

    return redirect('alumni_projects')



# ---------------- FACULTY ----------------
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
    projects = Project.objects.filter(faculty=request.user)
    return render(request, 'faculty_projects.html', {
        'projects': projects
    })


@role_required('alumni')
def mentor_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.alumni.add(request.user)
    messages.success(request, "You are now mentoring this project")
    return redirect('alumni_dashboard')




# ---------------- LOGOUT ----------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    profile = request.user.profile

    # STUDENT
    if profile.role == 'student':
        instance, created = StudentProfile.objects.get_or_create(
            profile=profile
        )
        form_class = StudentProfileForm

    # ALUMNI
    elif profile.role == 'alumni':
        instance, created = AlumniProfile.objects.get_or_create(
            profile=profile
        )
        form_class = AlumniProfileForm

    # FACULTY
    else:
        instance, created = FacultyProfile.objects.get_or_create(
            profile=profile
        )
        form_class = FacultyProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = form_class(instance=instance)

    return render(request, 'edit_profile.html', {
        'form': form
    })


@login_required
def view_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    student = None
    alumni = None
    faculty = None

    if profile.role == 'student':
        student = StudentProfile.objects.filter(profile=profile).first()

    elif profile.role == 'alumni':
        alumni = AlumniProfile.objects.filter(profile=profile).first()

    elif profile.role == 'faculty':
        faculty = FacultyProfile.objects.filter(profile=profile).first()

    return render(request, 'view_profile.html', {
        'profile': profile,
        'student': student,
        'alumni': alumni,
        'faculty': faculty,
    })