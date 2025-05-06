# Attendify: QR-Based Attendance Management System

## Team Members
- Sahil Raj (2401410004)
- Nirmit Dudeja (2401410022)
- Pallavi Baiju (2401410030)
- Dhuruv (2401410032)

## Project Description
Attendify is a web-based QR code attendance tracking system designed for educational institutions. It streamlines the attendance process by allowing teachers to generate unique QR codes for each class session, which students can scan using their devices to mark their attendance. The system provides real-time attendance tracking, comprehensive reporting, and user-friendly interfaces for administrators, teachers, and students.

## [Video Explanation]
[![Watch the Video](https://raw.githubusercontent.com/thesahilraj/attendify/refs/heads/main/FILES/screenshots/teacher-dashboard.png)](https://github.com/)

## Technologies Used
- **Backend**: Python (Django 5.1.7)
- **Database**: MySQL (via `mysqlclient`)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, crispy-bootstrap5
- **QR Generation**: `qrcode` Python package
- **QR Scanning**: Instascan
- **Image Handling**: Pillow
- **Forms**: django-crispy-forms
- **Tables**: DataTables
- 
## Features
- **User Authentication**: Secure login for administrators, teachers, and students
- **Role-Based Access Control**: Different interfaces and permissions for each user type
- **QR Code Generation**: Teachers can generate unique, time-limited QR codes for attendance
- **QR Code Scanning**: Students can scan QR codes using their device cameras
- **Class Management**: Create, edit, and archive classes
- **Student Enrollment**: Manage student enrollments in classes
- **Attendance Reports**: Comprehensive attendance reporting and analytics
- **Responsive Design**: Works on desktop and mobile devices

## Installation & Setup

### Requirements
- Python 3.10 or higher
- Django 5.1.7
- MySQL 5.7 or higher
- Virtual environment tool (optional but recommended)

### Installation Steps
1. **Clone the repository**
   git clone https://github.com/thesahilraj/attendify.git
   cd attendify

2. **Create a virtual environment (optional but recommended)**
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install dependencies**
   pip install -r requirements.txt

4. **Configure database**
   Update `settings.py` with your MySQL database credentials under `DATABASES`

5. **Apply migrations**
   python manage.py migrate

6. **Create superuser (admin)**
   python manage.py createsuperuser

7. **Run the server**
   python manage.py runserver

### Default Login Credentials
- **Administrator**: 
  - Username: admin
  - Password: admin123
- **Teacher**:
  - Username: teacher
  - Password: teacher123
- **Student**:
  - Username: student
  - Password: student123

## Usage
1. **Teachers**:
   - Log in with your teacher credentials
   - Create a new class or select an existing class
   - Generate a QR code for attendance
   - Display the QR code for students to scan

2. **Students**:
   - Log in with your student credentials
   - Navigate to the scan QR code page
   - Scan the QR code displayed by the teacher
   - Verify that your attendance has been marked

3. **Administrators**:
   - Log in with your admin credentials
   - Manage users, classes, and system settings
   - View attendance reports and statistics

## Security Features
- Password hashing using bcrypt
- CSRF protection for forms
- Input sanitization and validation
- Role-based access control
- Session security measures

## Acknowledgements
- Bootstrap for the responsive UI framework
- Instascan.js for the QR code scanning functionality
- DataTables for enhanced table functionality
