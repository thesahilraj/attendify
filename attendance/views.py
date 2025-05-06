from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.conf import settings
import uuid

from accounts.decorators import teacher_required, student_required
from .models import Course, ClassSession, QRCode, Attendance
from .forms import CourseForm, ClassSessionForm, QRCodeScanForm, AttendanceFilterForm

# Teacher views
@method_decorator(teacher_required, name='dispatch')
class CourseListView(ListView):
    """
    View for listing courses created by the teacher
    """
    model = Course
    template_name = 'attendance/teacher/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

@method_decorator(teacher_required, name='dispatch')
class CourseCreateView(CreateView):
    """
    View for creating a new course
    """
    model = Course
    form_class = CourseForm
    template_name = 'attendance/teacher/course_form.html'
    success_url = reverse_lazy('course_list')
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

@method_decorator(teacher_required, name='dispatch')
class CourseUpdateView(UpdateView):
    """
    View for updating a course
    """
    model = Course
    form_class = CourseForm
    template_name = 'attendance/teacher/course_form.html'
    success_url = reverse_lazy('course_list')
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)

@method_decorator(teacher_required, name='dispatch')
class CourseDeleteView(DeleteView):
    """
    View for deleting a course
    """
    model = Course
    template_name = 'attendance/teacher/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully!')
        return super().delete(request, *args, **kwargs)

@method_decorator(teacher_required, name='dispatch')
class CourseDetailView(DetailView):
    """
    View for viewing course details
    """
    model = Course
    template_name = 'attendance/teacher/course_detail.html'
    context_object_name = 'course'
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = ClassSession.objects.filter(course=self.object).order_by('-date', '-start_time')
        return context

@method_decorator(teacher_required, name='dispatch')
class ClassSessionCreateView(CreateView):
    """
    View for creating a new class session
    """
    model = ClassSession
    form_class = ClassSessionForm
    template_name = 'attendance/teacher/session_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['teacher'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        course_id = self.kwargs.get('course_id')
        if course_id:
            initial['course'] = get_object_or_404(Course, id=course_id, teacher=self.request.user)
        return initial
    
    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.object.course.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Class session created successfully!')
        return super().form_valid(form)

@method_decorator(teacher_required, name='dispatch')
class ClassSessionUpdateView(UpdateView):
    """
    View for updating a class session
    """
    model = ClassSession
    form_class = ClassSessionForm
    template_name = 'attendance/teacher/session_form.html'
    
    def get_queryset(self):
        return ClassSession.objects.filter(course__teacher=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['teacher'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.object.course.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Class session updated successfully!')
        return super().form_valid(form)

@method_decorator(teacher_required, name='dispatch')
class ClassSessionDeleteView(DeleteView):
    """
    View for deleting a class session
    """
    model = ClassSession
    template_name = 'attendance/teacher/session_confirm_delete.html'
    
    def get_queryset(self):
        return ClassSession.objects.filter(course__teacher=self.request.user)
    
    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.object.course.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Class session deleted successfully!')
        return super().delete(request, *args, **kwargs)

@method_decorator(teacher_required, name='dispatch')
class ClassSessionDetailView(DetailView):
    """
    View for viewing class session details and attendance
    """
    model = ClassSession
    template_name = 'attendance/teacher/session_detail.html'
    context_object_name = 'session'
    
    def get_queryset(self):
        return ClassSession.objects.filter(course__teacher=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendances'] = Attendance.objects.filter(session=self.object).select_related('student')
        context['qr_code'] = self.object.qr_codes.filter(is_active=True).last()
        context['qr_code_expiration_seconds'] = settings.QR_CODE_EXPIRATION_SECONDS
        return context

@login_required
@teacher_required
def generate_qr_code(request, session_id):
    """
    View for generating a new QR code for a class session
    """
    session = get_object_or_404(ClassSession, id=session_id, course__teacher=request.user)
    
    # Deactivate all existing QR codes for this session
    QRCode.objects.filter(session=session, is_active=True).update(is_active=False)
    
    # Create a new QR code
    qr_code = QRCode.objects.create(
        session=session,
        expires_at=timezone.now() + timezone.timedelta(seconds=settings.QR_CODE_EXPIRATION_SECONDS)
    )
    
    return redirect('session_detail', pk=session.id)

@login_required
@teacher_required
def refresh_qr_code(request, qr_id):
    """
    View for refreshing an existing QR code
    """
    old_qr_code = get_object_or_404(QRCode, id=qr_id, session__course__teacher=request.user)
    session = old_qr_code.session
    
    # Deactivate the old QR code
    old_qr_code.is_active = False
    old_qr_code.save()
    
    # Create a new QR code with a new UUID
    new_qr_code = QRCode.objects.create(
        session=session,
        code=uuid.uuid4(),
        expires_at=timezone.now() + timezone.timedelta(seconds=settings.QR_CODE_EXPIRATION_SECONDS)
    )
    
    return JsonResponse({
        'success': True,
        'expires_at': new_qr_code.expires_at.isoformat(),
        'image_url': new_qr_code.image.url,
        'code': str(new_qr_code.code),
        'expiration_seconds': settings.QR_CODE_EXPIRATION_SECONDS
    })

@login_required
@teacher_required
def attendance_report(request, course_id=None):
    """
    View for generating attendance reports
    """
    teacher = request.user
    form = AttendanceFilterForm(request.GET, teacher=teacher)
    
    courses = Course.objects.filter(teacher=teacher)
    attendances = Attendance.objects.filter(session__course__teacher=teacher)
    
    if course_id:
        course = get_object_or_404(Course, id=course_id, teacher=teacher)
        attendances = attendances.filter(session__course=course)
        form.initial['course'] = course
    
    if form.is_valid():
        if form.cleaned_data.get('course'):
            attendances = attendances.filter(session__course=form.cleaned_data['course'])
        
        if form.cleaned_data.get('date_from'):
            attendances = attendances.filter(session__date__gte=form.cleaned_data['date_from'])
        
        if form.cleaned_data.get('date_to'):
            attendances = attendances.filter(session__date__lte=form.cleaned_data['date_to'])
    
    attendances = attendances.select_related('student', 'session', 'session__course')
    
    return render(request, 'attendance/teacher/attendance_report.html', {
        'form': form,
        'attendances': attendances,
        'courses': courses
    })

# Student views
@method_decorator(student_required, name='dispatch')
class StudentCourseListView(ListView):
    """
    View for listing courses available to students
    """
    model = Course
    template_name = 'attendance/student/course_list.html'
    context_object_name = 'courses'

@method_decorator(student_required, name='dispatch')
class StudentAttendanceListView(ListView):
    """
    View for listing student's attendance records
    """
    model = Attendance
    template_name = 'attendance/student/attendance_list.html'
    context_object_name = 'attendances'
    
    def get_queryset(self):
        return Attendance.objects.filter(student=self.request.user).select_related('session', 'session__course')

@login_required
@student_required
def scan_qr_code(request):
    """
    View for scanning QR codes
    """
    if request.method == 'POST':
        form = QRCodeScanForm(request.POST)
        if form.is_valid():
            qr_code_uuid = form.cleaned_data['qr_code']
            
            try:
                qr_code = QRCode.objects.get(code=qr_code_uuid, is_active=True)
                
                # Check if QR code is expired
                if qr_code.is_expired:
                    messages.error(request, 'QR code has expired. Please ask your teacher to generate a new one.')
                    return redirect('scan_qr_code')
                
                # Check if session is ongoing
                if not qr_code.session.is_ongoing:
                    messages.error(request, 'Class session is not active or has ended.')
                    return redirect('scan_qr_code')
                
                # Mark attendance
                try:
                    attendance = Attendance.objects.create(
                        student=request.user,
                        session=qr_code.session,
                        qr_code=qr_code,
                        is_present=True
                    )
                    messages.success(request, f'Attendance marked successfully for {qr_code.session}')
                    return redirect('student_attendance_list')
                except IntegrityError:
                    messages.error(request, 'You have already marked your attendance for this session.')
                    return redirect('scan_qr_code')
                
            except QRCode.DoesNotExist:
                messages.error(request, 'Invalid QR code. Please try again.')
                return redirect('scan_qr_code')
    else:
        form = QRCodeScanForm()
    
    return render(request, 'attendance/student/scan_qr_code.html', {'form': form}) 