from django import forms
from .models import Course, ClassSession, Attendance, QRCode

class CourseForm(forms.ModelForm):
    """
    Form for creating and updating courses
    """
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course Description', 'rows': 3}),
        }

class ClassSessionForm(forms.ModelForm):
    """
    Form for creating and updating class sessions
    """
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    
    class Meta:
        model = ClassSession
        fields = ['course', 'date', 'start_time', 'end_time', 'room', 'notes']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room Number'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Session Notes', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher)

class QRCodeScanForm(forms.Form):
    """
    Form for scanning QR codes
    """
    qr_code = forms.UUIDField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'QR Code'})
    )

class AttendanceFilterForm(forms.Form):
    """
    Form for filtering attendance records
    """
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher) 