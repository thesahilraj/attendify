from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import UserLoginForm, StudentRegistrationForm, TeacherRegistrationForm
from .models import User
from .decorators import student_required, teacher_required

def login_view(request):
    """
    View for user login
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    View for user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def register_view(request):
    """
    View for registration landing page
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'accounts/register.html')

class StudentRegistrationView(CreateView):
    """
    View for student registration
    """
    template_name = 'accounts/student_registration.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now login.')
        return response
    
    def form_invalid(self, form):
        # Debug form errors
        print("Form errors:", form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class TeacherRegistrationView(CreateView):
    """
    View for teacher registration
    """
    template_name = 'accounts/teacher_registration.html'
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now login.')
        return response
    
    def form_invalid(self, form):
        # Debug form errors
        print("Form errors:", form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

@login_required
def dashboard_view(request):
    """
    View for user dashboard
    """
    if request.user.is_teacher:
        return redirect('teacher_dashboard')
    elif request.user.is_student:
        return redirect('student_dashboard')
    else:
        return redirect('admin:index')

@method_decorator(teacher_required, name='dispatch')
class TeacherDashboardView(TemplateView):
    """
    Dashboard view for teachers
    """
    template_name = 'accounts/teacher_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add teacher-specific context data here
        return context

@method_decorator(student_required, name='dispatch')
class StudentDashboardView(TemplateView):
    """
    Dashboard view for students
    """
    template_name = 'accounts/student_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add student-specific context data here
        return context
