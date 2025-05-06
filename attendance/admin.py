from django.contrib import admin
from .models import Course, ClassSession, QRCode, Attendance

class ClassSessionInline(admin.TabularInline):
    model = ClassSession
    extra = 0

class QRCodeInline(admin.TabularInline):
    model = QRCode
    extra = 0
    readonly_fields = ('code', 'image', 'created_at', 'expires_at')

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ('timestamp',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher', 'created_at')
    list_filter = ('teacher',)
    search_fields = ('code', 'name', 'teacher__username')
    inlines = [ClassSessionInline]

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'start_time', 'end_time', 'is_active')
    list_filter = ('course', 'date', 'is_active')
    search_fields = ('course__code', 'course__name', 'room')
    inlines = [QRCodeInline, AttendanceInline]

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('session', 'code', 'created_at', 'expires_at', 'is_active', 'is_expired')
    list_filter = ('session__course', 'is_active')
    readonly_fields = ('code', 'image', 'created_at', 'expires_at')
    search_fields = ('session__course__code', 'session__course__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'timestamp', 'is_present')
    list_filter = ('session__course', 'is_present', 'timestamp')
    search_fields = ('student__username', 'session__course__code', 'session__course__name')
    readonly_fields = ('timestamp',)
