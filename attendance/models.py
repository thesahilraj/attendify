from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Course(models.Model):
    """
    Model for courses
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class ClassSession(models.Model):
    """
    Model for class sessions
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.date} ({self.start_time} to {self.end_time})"
    
    @property
    def is_ongoing(self):
        now = timezone.now()
        session_date = self.date
        session_start = timezone.make_aware(timezone.datetime.combine(session_date, self.start_time))
        session_end = timezone.make_aware(timezone.datetime.combine(session_date, self.end_time))
        return session_start <= now <= session_end and self.is_active

class QRCode(models.Model):
    """
    Model for QR codes
    """
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='qr_codes')
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"QR Code for {self.session} - {self.code}"
    
    def save(self, *args, **kwargs):
        # Set expiration time to the configured seconds from now
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(seconds=settings.QR_CODE_EXPIRATION_SECONDS)
        
        # Generate QR code image
        if not self.image:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(self.code))
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.image.save(f"qr_{self.code}.png", File(buffer), save=False)
        
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at or not self.is_active

class Attendance(models.Model):
    """
    Model for attendance records
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='attendances')
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True, related_name='attendances')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'session']
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.student.username} - {self.session} - {'Present' if self.is_present else 'Absent'}"
