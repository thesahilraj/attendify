from django.urls import path
from . import views

urlpatterns = [
    # Teacher URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    path('sessions/create/', views.ClassSessionCreateView.as_view(), name='session_create'),
    path('sessions/create/<int:course_id>/', views.ClassSessionCreateView.as_view(), name='session_create_for_course'),
    path('sessions/<int:pk>/', views.ClassSessionDetailView.as_view(), name='session_detail'),
    path('sessions/<int:pk>/update/', views.ClassSessionUpdateView.as_view(), name='session_update'),
    path('sessions/<int:pk>/delete/', views.ClassSessionDeleteView.as_view(), name='session_delete'),
    
    path('sessions/<int:session_id>/generate-qr/', views.generate_qr_code, name='generate_qr_code'),
    path('qr-codes/<int:qr_id>/refresh/', views.refresh_qr_code, name='refresh_qr_code'),
    
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    path('attendance/report/<int:course_id>/', views.attendance_report, name='attendance_report_course'),
    
    # Student URLs
    path('student/courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
    path('student/attendance/', views.StudentAttendanceListView.as_view(), name='student_attendance_list'),
    path('student/scan-qr/', views.scan_qr_code, name='scan_qr_code'),
] 