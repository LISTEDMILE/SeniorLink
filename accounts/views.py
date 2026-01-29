from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
    return render(request, 'student_dashboard.html')

@login_required
def alumni_dashboard(request):
    return render(request, 'alumni_dashboard.html')

@login_required
def faculty_dashboard(request):
    return render(request, 'faculty_dashboard.html')