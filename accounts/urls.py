from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/student/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('register/teacher/', views.TeacherRegistrationView.as_view(), name='teacher_registration'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/teacher/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('dashboard/student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
] 