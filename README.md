# Attendify: QR-Based Attendance Management System

## Team Members
- [Your Name]
- [Team Member 2 Name] (if applicable)
- [Team Member 3 Name] (if applicable)

## Project Description
Attendify is a web-based QR code attendance tracking system designed for educational institutions. It streamlines the attendance process by allowing teachers to generate unique QR codes for each class session, which students can scan using their devices to mark their attendance. The system provides real-time attendance tracking, comprehensive reporting, and user-friendly interfaces for administrators, teachers, and students.

## [Video Explanation](https://youtu.be/your-video-id)
*Please replace the link above with your actual video explanation URL*

## Technologies Used
- **Backend**: PHP (Procedural & OOP)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **QR Generation**: Google Charts API
- **QR Scanning**: Instascan.js
- **Data Visualization**: Chart.js
- **Tables**: DataTables

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
- PHP 7.4 or higher
- MySQL 5.7 or higher
- Web server (Apache/Nginx)

### Installation Steps
1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/attendify.git
   cd attendify
   ```

2. **Database Setup**
   - Create a MySQL database
   - Import the database schema from `database/schema.sql`

3. **Configuration**
   - Edit `config/database.php` with your database credentials:
     ```php
     define('DB_HOST', 'your_database_host');
     define('DB_USER', 'your_database_username');
     define('DB_PASS', 'your_database_password');
     define('DB_NAME', 'your_database_name');
     ```
   - Edit `config/config.php` for site configuration if needed

4. **Directory Permissions**
   - Ensure the `uploads` directory and its subdirectories are writable:
     ```
     chmod -R 755 uploads/
     ```

5. **Web Server Configuration**
   - Point your web server to the project directory
   - Ensure .htaccess is properly configured for Apache

6. **Access the Application**
   - Navigate to `http://your-server/attendify` in your web browser
   - Use the installation wizard if it's the first time running the application

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

## License
[Your License Information]

## Acknowledgements
- Bootstrap for the responsive UI framework
- Instascan.js for the QR code scanning functionality
- Chart.js for data visualization
- DataTables for enhanced table functionality 