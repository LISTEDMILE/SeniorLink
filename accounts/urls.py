from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('student/', views.student_dashboard, name='student_dashboard'),
    path('alumni/', views.alumni_dashboard, name='alumni_dashboard'),
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('create-project/', views.create_project, name='create_project'),
    path('student/', views.student_dashboard, name='student_dashboard'),
path('request-mentorship/<int:alumni_id>/', views.send_mentorship_request, name='request_mentorship'),
path(
    'accept-mentorship/<int:request_id>/',
    views.accept_mentorship_request,
    name='accept_mentorship'
),
path('student/projects/', views.student_projects, name='student_projects'),
path('join-project/<int:project_id>/', views.join_project, name='join_project'),
path('faculty/projects/', views.faculty_projects, name='faculty_projects'),
path('logout/', views.logout_view, name='logout'),
path('edit_profile/', views.edit_profile, name='edit_profile'),
path('profile/<int:profile_id>/', views.view_profile, name='view_profile'),
path('alumni/projects/', views.alumni_projects, name='alumni_projects'),
path('alumni/projects/join/<int:project_id>/', views.join_project_as_alumni, name='join_project_as_alumni'),

]
