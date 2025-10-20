"""
CLI Application for Student and Course Management System

Allows you to manage students, courses, and enrollments
directly from the terminal.
"""

import sys
from sqlalchemy.orm import sessionmaker
from lib.db import engine
from lib.student import Student
from lib.course import Course
from lib.enrollment import Enrollment

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# STUDENT FUNCTIONS

# prompts user input and saves a new student record to the database
def add_student():
    """Add a new student"""
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    email = input("Enter email: ").strip()
    # Create a new Student object (an instance of the Student model)
    student = Student(first_name=first_name, last_name=last_name, email=email)
    # Add the student object to the current database session (stage it for saving)
    session.add(student)
    # Commit (save) the transaction to permanently store the student in the database
    session.commit()
    # Confirm success to the user
    print(f" Student {first_name} {last_name} added successfully!")


# fetch and display all students stored in the database
def list_students():
    """List all students"""
    # Retrieve all student records from the database using SQLAlchemy ORM
    students = session.query(Student).all()
    # Print a simple header for readability
    print("\n--- Students ---")
    # Loop through each student object and display their details
    for s in students:
        print(f"{s.id}. {s.first_name} {s.last_name} ({s.email})")
    # Print a footer line to mark the end of the list
    print("----------------\n")


# remove a student record from the database using their ID
def delete_student():
    """Delete a student by ID"""
    # Prompt the user to enter the student's ID (convert input from string to integer)
    student_id = int(input("Enter student ID to delete: "))
    # fetch the student in the database by their primary key (ID)
    student = session.get(Student, student_id)
    # If no student with that ID exists, show a message and exit the function
    if not student:
        print(" Student not found.")
        return
    # If found, mark the student object for deletion
    session.delete(student)
    session.commit()
    print(" Student deleted successfully.")


def update_student():
    """Update a student's details"""
    list_students()
    student_id = int(input("Enter student ID to update: "))
    student = session.get(Student, student_id)
    if not student:
        print(" Student not found.")
        return

    print(" Leave a field blank to keep the current value.")
    first_name = input(f"Enter new first name ({student.first_name}): ").strip() or student.first_name
    last_name = input(f"Enter new last name ({student.last_name}): ").strip() or student.last_name
    email = input(f"Enter new email ({student.email}): ").strip() or student.email

    student.first_name = first_name
    student.last_name = last_name
    student.email = email
    session.commit()
    print(" Student updated successfully.")


# COURSE FUNCTIONS


def add_course():
    """Add a new course"""
    """
    Add a new course.

    Steps:
    1. Prompt the user for course details (code, name, description, credits).
    2. Create a new Course object using the provided input.
    3. Add the course to the current database session.
    4. Commit the session to save the course permanently in the database.
    5. Display a success message to confirm the operation.
    """
    code = input("Enter course code: ").strip().upper()
    name = input("Enter course name: ").strip()
    description = input("Enter description: ").strip()
    credits = int(input("Enter number of credits: "))

    course = Course(code=code, name=name, description=description, credits=credits)
    session.add(course)
    session.commit()
    print(f" Course '{name}' added successfully!")


def list_courses():
    """List all courses"""
    """"
    Steps:
    1. Retrieve all course records from the database.
    2. Display a formatted list of courses showing:
       - ID
       - Course code
       - Course name
       - Number of credits
    3. Print header and footer lines for clarity in terminal output.
    """
    courses = session.query(Course).all()
    print("\n--- Courses ---")
    for c in courses:
        print(f"{c.id}. {c.code} - {c.name} ({c.credits} credits)")
    print("----------------\n")


def delete_course():
    """Delete a course by ID"""
    """"
    Steps:
    1. Prompt the user to enter the course ID to delete.
    2. Search the database for a course with the provided ID.
    3. If no course is found, display a 'Course not found' message and exit.
    4. If found, delete the course from the session.
    5. Commit the session to permanently remove the course from the database.
    6. Display a success message confirming the deletion.
    """
    course_id = int(input("Enter course ID to delete: "))
    course = session.get(Course, course_id)
    if not course:
        print(" Course not found.")
        return
    session.delete(course)
    session.commit()
    print(" Course deleted successfully.")


def update_course():
    """Update a course's details"""
    list_courses()
    course_id = int(input("Enter course ID to update: "))
    course = session.get(Course, course_id)
    if not course:
        print(" Course not found.")
        return

    print(" Leave a field blank to keep the current value.")
    code = input(f"Enter new course code ({course.code}): ").strip().upper() or course.code
    name = input(f"Enter new course name ({course.name}): ").strip() or course.name
    description = input(f"Enter new description ({course.description}): ").strip() or course.description
    credits_input = input(f"Enter new credits ({course.credits}): ").strip()
    credits = int(credits_input) if credits_input else course.credits

    course.code = code
    course.name = name
    course.description = description
    course.credits = credits
    session.commit()
    print(" Course updated successfully.")


# ENROLLMENT FUNCTIONS


def enroll_student():
    """
    Enroll a student in a course.

    Steps:
    1. Display a list of all available students.
    2. Prompt the user to enter the ID of the student to enroll.
    3. Display a list of all available courses.
    4. Prompt the user to enter the ID of the course to enroll the student in.
    5. Optionally accept a grade (leave blank if not applicable).
    6. Create a new Enrollment record linking the student and course.
    7. Add the enrollment to the session and commit it to save in the database.
    8. Display a confirmation message upon successful enrollment.
    """
    list_students()
    student_id = int(input("Enter student ID: "))
    list_courses()
    course_id = int(input("Enter course ID: "))
    grade = input("Enter grade (optional): ").strip() or None

    enrollment = Enrollment(student_id=student_id, course_id=course_id, grade=grade)
    session.add(enrollment)
    session.commit()
    print(" Student enrolled successfully!")


def list_enrollments():
    """
    List all enrollments.

    Steps:
    1. Retrieve all enrollment records from the database.
    2. For each enrollment:
       - Retrieve the associated student's full name.
       - Retrieve the associated course name.
       - Display the student's enrollment with their grade (or 'N/A' if missing).
    3. Handle missing student or course relationships gracefully by displaying 'N/A'.
    4. Print formatted output with header and footer lines for clarity.
    """
    enrollments = session.query(Enrollment).all()
    print("\n--- Enrollments ---")
    for e in enrollments:
        student_name = f"{e.student.first_name} {e.student.last_name}" if e.student else "N/A"
        course_name = e.course.name if e.course else "N/A"
        print(f"{e.id}. {student_name} -> {course_name} (Grade: {e.grade or 'N/A'})")
    print("----------------\n")


def delete_enrollment():
    """
    Delete an enrollment by ID.

    Steps:
    1. Prompt the user to enter the enrollment ID they want to delete.
    2. Search the database for the enrollment with the provided ID.
    3. If no enrollment is found, display a 'Enrollment not found' message and stop.
    4. If found, delete the enrollment record from the session.
    5. Commit the session to permanently remove the enrollment from the database.
    6. Display a confirmation message upon successful deletion.
    """
    enrollment_id = int(input("Enter enrollment ID to delete: "))
    enrollment = session.get(Enrollment, enrollment_id)
    if not enrollment:
        print(" Enrollment not found.")
        return
    session.delete(enrollment)
    session.commit()
    print(" Enrollment deleted successfully.")


def update_enrollment():
    """Update an enrollment's grade"""
    list_enrollments()
    enrollment_id = int(input("Enter enrollment ID to update: "))
    enrollment = session.get(Enrollment, enrollment_id)
    if not enrollment:
        print(" Enrollment not found.")
        return

    grade = input(f"Enter new grade ({enrollment.grade or 'N/A'}): ").strip() or enrollment.grade
    enrollment.grade = grade
    session.commit()
    print(" Enrollment updated successfully.")


# MAIN MENU


def main_menu():
    while True:
        print("""
📚 STUDENT & COURSE MANAGEMENT SYSTEM
====================================
1️⃣  Add Student
2️⃣  List Students
3️⃣  Delete Student
4️⃣  Add Course
5️⃣  List Courses
6️⃣  Delete Course
7️⃣  Enroll Student in Course
8️⃣  List Enrollments
9️⃣  Delete Enrollment
🔟  Update Student
1️⃣1️⃣  Update Course
1️⃣2️⃣  Update Enrollment
0️⃣  Exit
""")
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            list_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            add_course()
        elif choice == "5":
            list_courses()
        elif choice == "6":
            delete_course()
        elif choice == "7":
            enroll_student()
        elif choice == "8":
            list_enrollments()
        elif choice == "9":
            delete_enrollment()
        elif choice == "10":
            update_student()
        elif choice == "11":
            update_course()
        elif choice == "12":
            update_enrollment()
        elif choice == "0":
            print("👋 Goodbye!")
            session.close()
            sys.exit()
        else:
            print(" Invalid choice, try again.")


if __name__ == "__main__":
    main_menu()
