from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('student/', views.student_dashboard, name='student_dashboard'),
    path('alumni/', views.alumni_dashboard, name='alumni_dashboard'),
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('create-project/', views.create_project, name='create_project'),
]
