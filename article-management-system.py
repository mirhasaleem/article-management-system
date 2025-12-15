import sys
import json
from pathlib import Path
from datetime import datetime
import os

# Uncomment, if you are so brave
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Constants for file paths
JSON_DATA_DIR = Path("json_data")
LOGIN_HISTORY_FILE = JSON_DATA_DIR / "login_history.json"
USER_DATA_FILE = JSON_DATA_DIR / "user_data.json"
SUBMISSIONS_DIR = Path("submissions")
GRADES_FILE = JSON_DATA_DIR / 'grades.json'
SUBMISSION_HISTORY_FILE = JSON_DATA_DIR / "submission_history.json"


def safe_exit():
    print("Exiting. Thank you for using the article management system :)")
    sys.exit(1)


def read_json(path):
    if isinstance(path, str):
        path = Path(path)
    with path.open(encoding="utf8") as f:
        return json.load(f)


def save_json(path, data):
    if isinstance(path, str):
        path = Path(path)
    with path.open("w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _ensure_directories_exist():
    JSON_DATA_DIR.mkdir(exist_ok=True)
    SUBMISSIONS_DIR.mkdir(exist_ok=True)


def login():
    userid = input("Enter your user id: ")
    password = input("Enter your password: ")
    if _login_successful(userid, password):
        print("Login successful")
        _log_login_attempt(userid, True)
        return True
    else:
        print("Login failed")
        _log_login_attempt(userid, False)
        safe_exit()


def _login_successful(userid, password):
    if (userid == "admin" and password == "ZDHH"):
        return True
    else:
        try:
            users = read_json(USER_DATA_FILE)
        except FileNotFoundError:
            print("No user data found.")
            return False

        return users.get(userid) == password


def load_all_grades():
    try:
        return read_json(GRADES_FILE)
    except FileNotFoundError:
        return {}


def _log_login_attempt(userid, success):
    try:
        history = read_json(LOGIN_HISTORY_FILE)
    except FileNotFoundError:
        history = []

    history.append({
        "userid": userid,
        "timestamp": datetime.now().isoformat(),
        "success": success
    })

    save_json(LOGIN_HISTORY_FILE, history)


def add_user():
    new_userid = input("Enter the new user id: ")
    new_password = input("Enter the new password: ")
    _add_new_user(new_userid, new_password)


def _add_new_user(new_userid, new_password):
    try:
        users = read_json(USER_DATA_FILE)
    except FileNotFoundError:
        users = {}

    users[new_userid] = new_password
    save_json(USER_DATA_FILE, users)
    print("User added successfully.")


def show_start_prompt():
    prompt = '''
    Welcome to the article management system! Type in the number of the action you want to perform:
    1. Help
    2. Add user
    3. Exit
    4. Add a submission from student
    5. Grade a student's submission
    6. List all submissions
    7. List all submissions have not been graded
    8. Display the average score
    9. Display the student who has the highest score
    10. Display the students whose score is less than a threshold
    11. Send emails to students notifying them of their grades (Optional)
    12. Store the grade to a json file
    13. Load the grade from a json file
    14. Delete a submission and its grade
    '''
    print(prompt)


def is_valid_user_choice(user_choice):
    return user_choice.isdigit() and 1 <= int(user_choice) <= 14


def main():
    all_grade = load_all_grades()
    login()
    show_start_prompt()

    actions = {
        "1": show_help_info,
        "2": add_user,
        "3": safe_exit,
        "4": add_submission,
        "5": lambda: grade_a_submission(),
        "6": lambda: list_all_submissions(),
        "7": lambda: list_submissions_to_grade(),
        "8": lambda: display_average_score(all_grade),
        "9": lambda: display_highest_score(all_grade),
        "10": lambda: display_grade_less_than_threshold(all_grade),
        "11": lambda: email_notification(),
        "12": lambda: store_grade(all_grade),
        "13": lambda: load_grade(all_grade),
        "14": lambda: delete_submission(all_grade)
    }

    while True:
        user_choice = input("Enter your choice: ")
        if not is_valid_user_choice(user_choice):
            print("Invalid choice; Try again...")
            continue

        action = actions.get(user_choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Invalid choice; Try again...")


def add_submission():
    student_id = input("Enter the student id: ")
    assignment_id = input("Enter the assignment id: ")
    submission_path = input("Enter the submission path: ")
    _add_submission(student_id, assignment_id, submission_path)
    _log_submission(student_id, assignment_id, submission_path)


def _add_submission(student_id, assignment_id, submission_path_local):
    submission_path = f"./submissions/{submission_path_local}"
    if not os.path.exists(submission_path):
        print("Specified submission file path does not exist.")
        return False

    file_extension = os.path.splitext(submission_path)[1]
    new_file_name = f"{student_id}_{assignment_id}{file_extension}"
    destination_path = SUBMISSIONS_DIR / new_file_name

    try:
        with open(submission_path, 'rb') as source_file:
            file_content = source_file.read()

        with open(destination_path, 'wb') as dest_file:
            dest_file.write(file_content)

        print("Submission file copied successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while copying the submission file: {e}")
        return False


def _log_submission(student_id, assignment_id, submission_path):
    successful = _add_submission(student_id, assignment_id, submission_path)
    if not successful:
        return

    try:
        if SUBMISSION_HISTORY_FILE.exists():
            submission_history = read_json(SUBMISSION_HISTORY_FILE)
        else:
            submission_history = []

        submission_history.append({
            "student_id": student_id,
            "assignment_id": assignment_id,
            "submission_path": submission_path,
            "timestamp": datetime.now().isoformat()
        })

        save_json(SUBMISSION_HISTORY_FILE, submission_history)
    except Exception as e:
        print(f"An error occurred while logging the submission: {e}")


def read_grades():
    if not os.path.exists(GRADES_FILE):
        return {}
    with open(GRADES_FILE, 'r') as file:
        return json.load(file)


def write_grades(all_grade):
    with open(GRADES_FILE, 'w') as file:
        json.dump(all_grade, file, indent=4)


def grade_a_submission():
    all_grade = read_grades()
    student_id = input("Enter the student id: ")
    assignment_id = input("Enter the assignment id: ")
    _grade_a_submission(all_grade, student_id, assignment_id)
    write_grades(all_grade)


def _grade_a_submission(all_grade, student_id, assignment_id):
    file_path = f"./submissions/{student_id}_{assignment_id}.txt"

    if not os.path.exists(file_path):
        print("Specified submission file does not exist.")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print("File Content:")
            print(content)

        grade = int(input("Enter the grade: "))
        all_grade.setdefault(student_id, {})[assignment_id] = grade
        print("Grade added successfully.")
    except ValueError:
        print("Invalid grade input. Please enter a numeric value.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_all_submissions():
    try:
        submission_history = read_json(SUBMISSION_HISTORY_FILE)
        all_grade = read_grades()
    except FileNotFoundError as e:
        print(f"No submission history or grades found: {e}")
        return

    for submission in submission_history:
        student_id = submission['student_id']
        assignment_id = submission['assignment_id']
        grade = all_grade.get(student_id, {}).get(assignment_id, "Not Graded")
        print(
            f"Student ID: {student_id}, Assignment ID: {assignment_id}, Grade: {grade}")


def list_submissions_to_grade():
    try:
        submission_history = read_json(SUBMISSION_HISTORY_FILE)
        all_grade = read_grades()
    except FileNotFoundError as e:
        print(f"No submission history or grades found: {e}")
        return

    for submission in submission_history:
        student_id = submission['student_id']
        assignment_id = submission['assignment_id']
        # Checking for grade in grades.json
        if all_grade.get(student_id, {}).get(assignment_id, "") == "":
            print(f"Student ID: {student_id}, Assignment ID: {assignment_id}")


def display_average_score(all_grade):
    total_grades, num_grades = sum((g for a in all_grade.values() for g in a.values(
    ) if g != ""), 0), sum((g != "" for a in all_grade.values() for g in a.values()))
    print(
        f"Average Score: {total_grades / num_grades}" if num_grades else "No grades available.")


def display_highest_score(all_grade):
    highest_score, highest_student = 0, ""
    for student_id, assignments in all_grade.items():
        graded_assignments = [g for g in assignments.values() if g != ""]
        if graded_assignments:
            average_score = sum(graded_assignments) / len(graded_assignments)
            if average_score > highest_score:
                highest_score, highest_student = average_score, student_id

    print(
        f"Highest Score: {highest_score}, Student ID: {highest_student}" if highest_student else "No grades available.")


def display_grade_less_than_threshold(all_grade):
    threshold = float(input("Enter the threshold: "))
    for student_id, assignments in all_grade.items():
        grades = [grade for grade in assignments.values() if grade != ""]
        if grades:
            average_score = sum(grades) / len(grades)
            if average_score < threshold:
                print(
                    f"Student ID: {student_id}, Average Score: {average_score}")


def email_notification():
    print("Email Sent without actually sending Email!!!!")
    # User input
    email = input("Enter the student's email: ")
    student_id = input("Enter the student id: ")
    assignment_id = input("Enter the assignment id: ")
    grade = input("Enter the grade: ")

    # Email content
    subject = f"Grade Notification for Assignment {assignment_id}"
    body = f"Hello,\n\nYour grade for the assignment '{assignment_id}' is: {grade}.\n\nBest regards,\nLogan Paul Gang fr"

    # Create a MIMEText object
    message = MIMEMultipart()
    message["From"] = ""
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Email
    try:
        with smtplib.SMTP("SMTP.SERVER.LINK.com", 587) as server:  # Replace with your SMTP server and port(replace 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("YOUR_EMAIL@ADDRESS.com", "YOUR_PASSWORD")
            server.sendmail("YOUR_EMAIL@ADDRESS.com", email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


def store_grade(all_grade):
    try:
        file_path = input("Enter the file path: ")
        save_json(file_path, all_grade)
        print("Grade stored successfully.")
    except Exception as e:
        print(f"Failed to store grade: {e}")


def load_grade(all_grade):
    try:
        file_path = input("Enter the file path: ")
        loaded_grade = read_json(file_path)
        all_grade.clear()
        all_grade.update(loaded_grade)
        print("Grade loaded successfully.")
    except Exception as e:
        print(f"Failed to load grade: {e}")


def delete_submission(all_grade):
    student_id = input("Enter the student id: ")
    assignment_id = input("Enter the assignment id: ")

    try:
        # Read the current submission history
        submission_history = read_json(SUBMISSION_HISTORY_FILE)

        # Find and remove the specific submission
        submission_history = [submission for submission in submission_history if not (
            submission['student_id'] == student_id and submission['assignment_id'] == assignment_id)]

        # Save the updated submission history
        save_json(SUBMISSION_HISTORY_FILE, submission_history)

        # Deleting the grade if it exists
        if assignment_id in all_grade.get(student_id, {}):
            del all_grade[student_id][assignment_id]

        print("Submission and its grade deleted successfully.")
    except FileNotFoundError:
        print("No submission history found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def show_help_info():
    show_start_prompt()


if __name__ == '__main__':
    _ensure_directories_exist()
    main()
