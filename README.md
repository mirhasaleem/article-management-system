# Article Management System

A command-line application for managing article submissions, grading, and student performance tracking. This system allows administrators to manage user accounts, collect student submissions, assign grades, and generate performance analytics.

## Features

### User Management
- **Login System**: Secure authentication with user IDs and passwords
- **Add Users**: Create new user accounts (admin only)
- **Login History**: Track all login attempts with timestamps

### Submission Management
- **Add Submissions**: Accept article submissions from students
- **List Submissions**: View all submissions with their grades
- **List Ungraded Submissions**: Quickly find submissions that need grading
- **Delete Submissions**: Remove submissions and associated grades
- **Submission History**: Maintain a log of all submissions

### Grading System
- **Grade Submissions**: Assign numerical grades to student submissions
- **Grade Storage**: Save grades to JSON files
- **Grade Loading**: Load grades from external JSON files
- **Grade Analytics**:
  - Calculate average scores across all submissions
  - Identify the highest-performing student
  - Find students below a performance threshold

### Optional Features
- **Email Notifications**: Send grade notifications to students (requires SMTP configuration)

## Project Structure

```
Article management system/
├── article-management-system.py   # Main application file
├── json_data/                     # Data storage directory
│   ├── user_data.json            # User credentials
│   ├── grades.json               # Student grades
│   ├── login_history.json        # Login attempt logs
│   └── submission_history.json   # Submission records
└── submissions/                   # Student submission files
    └── [student_id]_[assignment_id].txt
```

## Installation

### Requirements
- Python 3.7+

### Setup

1. Clone or download the project to your local machine
2. Navigate to the project directory
3. Run the application:
   ```bash
   python article-management-system.py
   ```

The application will automatically create the required directories (`json_data/` and `submissions/`) on first run.

## Usage

### Starting the Application

```bash
python article-management-system.py
```

### Login
- **Admin Account**:
  - User ID: `admin`
  - Password: `ZDHH`
- **Student/Regular Users**: Use credentials created by the admin

### Menu Options

| Option | Action |
|--------|--------|
| 1 | Display help/main menu |
| 2 | Add a new user account |
| 3 | Exit the application |
| 4 | Add a student submission |
| 5 | Grade a student's submission |
| 6 | List all submissions |
| 7 | List ungraded submissions |
| 8 | Display average score across all submissions |
| 9 | Display highest performing student |
| 10 | Find students below a score threshold |
| 11 | Send grade notifications via email |
| 12 | Save grades to a JSON file |
| 13 | Load grades from a JSON file |
| 14 | Delete a submission and its grade |

### Example Workflow

1. **Login** as admin with the credentials provided
2. **Add a user** (option 2) for a new student
3. **Add a submission** (option 4) - specify the student ID, assignment ID, and file path
4. **Grade the submission** (option 5) - enter student ID, assignment ID, and grade
5. **View analytics** (options 8-10) - check performance metrics
6. **Save grades** (option 12) - backup grades to a JSON file

## Data Files

### user_data.json
Stores user credentials in the format:
```json
{
  "student_id": "password",
  "admin": "ZDHH"
}
```

### grades.json
Stores grades organized by student and assignment:
```json
{
  "student_id": {
    "assignment_id": 85,
    "assignment_id_2": 90
  }
}
```

### submission_history.json
Maintains a log of all submissions:
```json
[
  {
    "student_id": "student1",
    "assignment_id": "A1",
    "submission_path": "student1_A1.txt",
    "timestamp": "2025-12-15T10:30:45.123456"
  }
]
```

### login_history.json
Records all login attempts:
```json
[
  {
    "userid": "admin",
    "timestamp": "2025-12-15T10:30:00.123456",
    "success": true
  }
]
```

## Email Notifications (Optional)

To enable email notifications, configure the SMTP settings in the `email_notification()` function:

1. Replace `SMTP.SERVER.LINK.com` with your SMTP server address
2. Replace `587` with the appropriate SMTP port
3. Replace `YOUR_EMAIL@ADDRESS.com` with your email address
4. Replace `YOUR_PASSWORD` with your email password

**Note**: The current implementation prints a message instead of actually sending emails for security reasons.

## Common Tasks

### Grading a Submission
1. Select option 5
2. Enter the student ID
3. Enter the assignment ID
4. Review the submission content displayed on screen
5. Enter the numerical grade

### Finding Low Performers
1. Select option 10
2. Enter the threshold score
3. The system displays all students with average scores below the threshold

### Backup Grades
1. Select option 12
2. Enter a file path for the backup (e.g., `backup_grades.json`)
3. Grades are saved to the specified location

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Specified submission file path does not exist" | Ensure the file exists at the specified path in the submissions folder |
| "Login failed" | Verify your user ID and password are correct |
| "No submission history or grades found" | Ensure submissions have been added and grades assigned |
| Email not sending | Check SMTP configuration and ensure credentials are correct |

## Future Enhancements

- Database support (instead of JSON files)
- Web-based interface
- Batch grade import/export
- Assignment deadlines and late submission tracking
- Student performance trends and reporting
- Multi-file submission support

## License

This project is provided as-is for educational and administrative purposes.

## Support

For issues or questions, please contact the system administrator.
