from university import University
from student import Student
from faculty import Faculty
from course import Course
from utils import log_action, student_id_generator
from pprint import pprint

# Initialize University
uni = University()
id_gen = student_id_generator()

def run_action(action):
    try:
        action()
    except ValueError as error:
        print(f"Error: {error}")

@log_action
def add_student():
    name = input("Enter student name: ")
    email = input("Enter student email: ")
    phone = input("Enter student phone: ")
    roll_no = next(id_gen)
    while uni.find_student(roll_no):
        roll_no = next(id_gen)
    dept = input("Enter department: ")
    sem = input("Enter semester: ")
    student = Student(name, email, phone, roll_no, dept, sem)
    student.generate_id()
    uni.add_student(student)
    print("Student added successfully!")

@log_action
def add_faculty():
    name = input("Enter faculty name: ")
    email = input("Enter faculty email: ")
    phone = input("Enter faculty phone: ")
    emp_id = input("Enter employee ID: ")
    dept = input("Enter department: ")
    salary = float(input("Enter salary: "))
    faculty = Faculty(name, email, phone, emp_id, dept, salary)
    faculty.generate_id()
    uni.add_faculty(faculty)
    print("Faculty added successfully!")

@log_action
def create_course():
    cid = input("Enter course ID: ")
    cname = input("Enter course name: ")
    credits = int(input("Enter credits: "))
    course = Course(cid, cname, credits)
    uni.create_course(course)
    print("Course created successfully!")

@log_action
def register_student_in_course():
    roll_no = input("Enter student roll number: ")
    cid = input("Enter course ID: ")
    student = uni.find_student(roll_no)
    if student:
        uni.register_student(student, cid)
        print("Student registered in course successfully!")
    else:
        print("Student not found.")

@log_action
def assign_faculty_to_course():
    emp_id = input("Enter faculty employee ID: ")
    cid = input("Enter course ID: ")
    print(uni.assign_faculty_to_course(emp_id, cid))

@log_action
def attendance_menu():
    print("1. Mark Attendance")
    print("2. View Attendance")
    choice = input("Enter choice: ")
    roll_no = input("Enter student roll number: ")
    cid = input("Enter course ID: ")

    if choice == "1":
        status = input("Is student present? (y/n): ").strip().lower()
        record = uni.mark_attendance(roll_no, cid, status != "n")
        print(record)
    elif choice == "2":
        record = uni.get_attendance(roll_no, cid)
        print(record if record else "No attendance record found.")
    else:
        print("Invalid choice.")

@log_action
def result_menu():
    print("1. Enter Marks")
    print("2. View Result")
    choice = input("Enter choice: ")
    roll_no = input("Enter student ID / roll number: ")

    if choice == "1":
        subject = input("Enter subject/course name: ")
        marks = float(input("Enter marks out of 100: "))
        result = uni.enter_marks(roll_no, subject, marks)
        print(result.generate_result())
    elif choice == "2":
        print(uni.get_result(roll_no))
    else:
        print("Invalid choice.")

@log_action
def pay_fee():
    roll_no = input("Enter student roll number: ")
    if roll_no not in uni.fee_records:
        total_fee = float(input("Enter total fee: "))
        uni.add_fee_record(roll_no, total_fee)
    amount = float(input("Enter amount to pay: "))
    print(uni.pay_fee(roll_no, amount))

@log_action
def library_menu():
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. Search Book")
    choice = input("Enter choice: ")
    if choice == "1":
        title = input("Enter book title: ")
        print(uni.library.add_book(title))
    elif choice == "2":
        sid = input("Enter student ID: ")
        title = input("Enter book title: ")
        print(uni.library.issue_book(sid, title))
    elif choice == "3":
        sid = input("Enter student ID: ")
        title = input("Enter book title: ")
        print(uni.library.return_book(sid, title))
    elif choice == "4":
        title = input("Enter book title: ")
        print(uni.library.search_book(title))
    else:
        print("Invalid choice.")

@log_action
def generate_report():
    pprint(uni.generate_report())

@log_action
def export_csv_reports():
    report_files = uni.export_csv_reports()
    print("CSV reports exported:")
    for name, path in report_files.items():
        print(f"{name}: {path}")

def main_menu():
    while True:
        print("\n--- Smart University Management System ---")
        print("1. Add Student")
        print("2. Add Faculty")
        print("3. Create Course")
        print("4. Register Student in Course")
        print("5. Assign Faculty to Course")
        print("6. Attendance Menu")
        print("7. Result Menu")
        print("8. Pay Fee")
        print("9. Library Menu")
        print("10. Generate Report")
        print("11. Export CSV Reports")
        print("12. Save Data")
        print("13. Load Data")
        print("14. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            run_action(add_student)
        elif choice == "2":
            run_action(add_faculty)
        elif choice == "3":
            run_action(create_course)
        elif choice == "4":
            run_action(register_student_in_course)
        elif choice == "5":
            run_action(assign_faculty_to_course)
        elif choice == "6":
            run_action(attendance_menu)
        elif choice == "7":
            run_action(result_menu)
        elif choice == "8":
            run_action(pay_fee)
        elif choice == "9":
            run_action(library_menu)
        elif choice == "10":
            run_action(generate_report)
        elif choice == "11":
            run_action(export_csv_reports)
        elif choice == "12":
            uni.save_data()
            print("Data saved successfully!")
        elif choice == "13":
            data = uni.load_data()
            print("Data loaded successfully!" if data else "No saved data found.")
        elif choice == "14":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
