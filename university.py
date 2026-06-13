from student import Student
from faculty import Faculty
from course import Course
from attendance import Attendance
from result import Result
from library import Library
from fee import Fee
import csv
import json
from pathlib import Path

class University:
    def __init__(self):
        self.students = []
        self.faculty = []
        self.courses = {}
        self.library = Library()
        self.fee_records = {}
        self.attendance_records = {}
        self.result_records = {}
        self.data_file = Path("data/university.json")
        self.csv_dir = Path("data/csv_reports")

    def _normalize_student_id(self, student_id):
        student_id = str(student_id).strip()
        if not student_id:
            return student_id

        student_id = student_id.upper()
        if student_id.isdigit():
            return f"S-{student_id}"
        if student_id.startswith("S") and len(student_id) > 1 and student_id[1:].isdigit():
            return f"S-{student_id[1:]}"
        return student_id

    def find_student(self, roll_no):
        roll_no = self._normalize_student_id(roll_no)
        return next(
            (
                student for student in self.students
                if self._normalize_student_id(student.roll_no) == roll_no
            ),
            None
        )

    def find_faculty(self, employee_id):
        return next((faculty for faculty in self.faculty if faculty.employee_id == employee_id), None)

    # Student Management
    def add_student(self, student):
        if self.find_student(student.roll_no):
            raise ValueError("Student roll number already exists.")
        self.students.append(student)

    # Faculty Management
    def add_faculty(self, faculty):
        if self.find_faculty(faculty.employee_id):
            raise ValueError("Faculty employee ID already exists.")
        self.faculty.append(faculty)

    # Course Management
    def create_course(self, course):
        if course.course_id in self.courses:
            raise ValueError("Course ID already exists.")
        self.courses[course.course_id] = course

    def register_student(self, student, course_id):
        if course_id not in self.courses:
            raise ValueError("Invalid course ID.")
        self.courses[course_id].add_student(student)
        student.register_course(course_id)

    def assign_faculty_to_course(self, employee_id, course_id):
        faculty = self.find_faculty(employee_id)
        if not faculty:
            raise ValueError("Faculty not found.")
        if course_id not in self.courses:
            raise ValueError("Invalid course ID.")
        faculty.assign_course(course_id)
        self.courses[course_id].assign_faculty(faculty)
        return f"{faculty._name} assigned to {self.courses[course_id].course_name}."

    # Attendance Management
    def _attendance_key(self, student_id, course_id):
        return f"{student_id}|{course_id}"

    def mark_attendance(self, student_id, course_id, present=True):
        student = self.find_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        if course_id not in self.courses:
            raise ValueError("Invalid course ID.")
        if course_id not in student.registered_courses:
            raise ValueError("Student is not registered in this course.")

        key = self._attendance_key(student_id, course_id)
        if key not in self.attendance_records:
            self.attendance_records[key] = Attendance(student_id, course_id)
        self.attendance_records[key].mark_attendance(present)
        return self.attendance_records[key]

    def get_attendance(self, student_id, course_id):
        return self.attendance_records.get(self._attendance_key(student_id, course_id))

    # Result Management
    def enter_marks(self, student_id, subject, marks):
        student_id = self._normalize_student_id(student_id)
        student = self.find_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        marks = float(marks)
        if student_id not in self.result_records:
            self.result_records[student_id] = Result(student_id)
        result = self.result_records[student_id]
        result.enter_marks(subject, marks)
        result.calculate_grade(subject)
        result.calculate_cgpa()
        student.results[subject] = marks / 10
        return result

    def _load_results_from_csv(self):
        results_file = self.csv_dir / "results.csv"
        try:
            with results_file.open(newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student_id = self._normalize_student_id(row.get("student_id", ""))
                    subject = row.get("subject", "").strip()
                    if not student_id or not subject:
                        continue

                    try:
                        marks = float(row.get("marks", 0))
                    except ValueError:
                        continue

                    if student_id not in self.result_records:
                        self.result_records[student_id] = Result(student_id)

                    result = self.result_records[student_id]
                    result.enter_marks(subject, marks)
                    grade = row.get("grade", "").strip()
                    result.grade[subject] = grade if grade else result.calculate_grade(subject)
                    result.calculate_cgpa()
        except FileNotFoundError:
            return

    def get_result(self, student_id):
        student_id = self._normalize_student_id(student_id)
        if student_id not in self.result_records:
            self._load_results_from_csv()
        if student_id not in self.result_records:
            raise ValueError("No result found for student.")
        result = self.result_records[student_id]
        result.calculate_cgpa()
        return result.generate_result()

    # Fee Management
    def add_fee_record(self, student_id, total_fee):
        if not self.find_student(student_id):
            raise ValueError("Student not found.")
        if student_id in self.fee_records:
            raise ValueError("Fee record already exists for student.")
        self.fee_records[student_id] = Fee(student_id, total_fee)

    def pay_fee(self, student_id, amount):
        if student_id not in self.fee_records:
            raise ValueError("No fee record found for student.")
        return self.fee_records[student_id].pay_fee(amount)

    # Reports
    def generate_report(self):
        return {
            "students": [s.display_details() for s in self.students],
            "faculty": [f.display_details() for f in self.faculty],
            "courses": [c.display_course() for c in self.courses.values()],
            "fees": [fee.generate_receipt() for fee in self.fee_records.values()],
            "attendance": [str(record) for record in self.attendance_records.values()],
            "results": [result.generate_result() for result in self.result_records.values()],
            "library": str(self.library)
        }

    # File Persistence
    def save_data(self):
        self.data_file.parent.mkdir(exist_ok=True)
        data = {
            "students": [s.__dict__ for s in self.students],
            "faculty": [f.__dict__ for f in self.faculty],
            "courses": {
                cid: {
                    "course_id": c.course_id,
                    "course_name": c.course_name,
                    "credits": c.credits,
                    "faculty_assigned": c.faculty_assigned.employee_id if c.faculty_assigned else None,
                    "students": [student.roll_no for student in c.students]
                }
                for cid, c in self.courses.items()
            },
            "library": {
                "books": self.library.books,
                "issued_books": self.library.issued_books
            },
            "fee_records": {
                sid: fee.generate_receipt()
                for sid, fee in self.fee_records.items()
            },
            "attendance_records": {
                key: record.__dict__
                for key, record in self.attendance_records.items()
            },
            "result_records": {
                sid: result.generate_result()
                for sid, result in self.result_records.items()
            }
        }
        with self.data_file.open("w") as f:
            json.dump(data, f, indent=4)

    def export_csv_reports(self):
        self.csv_dir.mkdir(parents=True, exist_ok=True)

        report_files = {
            "students": self.csv_dir / "students.csv",
            "faculty": self.csv_dir / "faculty.csv",
            "courses": self.csv_dir / "courses.csv",
            "fees": self.csv_dir / "fees.csv",
            "attendance": self.csv_dir / "attendance.csv",
            "results": self.csv_dir / "results.csv"
        }

        with report_files["students"].open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["person_id", "name", "email", "phone", "roll_no", "department", "semester", "registered_courses"])
            for student in self.students:
                writer.writerow([
                    student._person_id,
                    student._name,
                    student._email,
                    student._phone,
                    student.roll_no,
                    student.department,
                    student.semester,
                    ", ".join(student.registered_courses)
                ])

        with report_files["faculty"].open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["person_id", "name", "email", "phone", "employee_id", "department", "salary", "courses_taught"])
            for faculty in self.faculty:
                writer.writerow([
                    faculty._person_id,
                    faculty._name,
                    faculty._email,
                    faculty._phone,
                    faculty.employee_id,
                    faculty.department,
                    faculty.salary,
                    ", ".join(faculty.courses_taught)
                ])

        with report_files["courses"].open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["course_id", "course_name", "credits", "faculty_assigned", "students"])
            for course in self.courses.values():
                writer.writerow([
                    course.course_id,
                    course.course_name,
                    course.credits,
                    course.faculty_assigned.employee_id if course.faculty_assigned else "",
                    ", ".join(student.roll_no for student in course.students)
                ])

        with report_files["fees"].open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "total_fee", "paid_fee", "balance_fee"])
            for fee in self.fee_records.values():
                writer.writerow([fee.student_id, fee.total_fee, fee.paid_fee, fee.balance_fee])

        with report_files["attendance"].open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "course_id", "total_classes", "present_classes", "attendance_percentage"])
            for record in self.attendance_records.values():
                writer.writerow([
                    record.student_id,
                    record.course_id,
                    record.total_classes,
                    record.present_classes,
                    record.attendance_percentage()
                ])

        with report_files["results"].open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject", "marks", "grade", "cgpa"])
            for result in self.result_records.values():
                result.calculate_cgpa()
                for subject, marks in result.subject_marks.items():
                    writer.writerow([
                        result.student_id,
                        subject,
                        marks,
                        result.grade.get(subject, ""),
                        result.cgpa
                    ])

        return report_files

    def load_data(self):
        try:
            with self.data_file.open("r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        self.students = []
        for item in data.get("students", []):
            student = Student(
                item.get("_name", ""),
                item.get("_email", ""),
                item.get("_phone", ""),
                item.get("roll_no", ""),
                item.get("department", ""),
                item.get("semester", "")
            )
            student._person_id = item.get("_person_id")
            student.registered_courses = item.get("registered_courses", [])
            student.results = item.get("results", {})
            self.students.append(student)

        self.faculty = []
        for item in data.get("faculty", []):
            faculty = Faculty(
                item.get("_name", ""),
                item.get("_email", ""),
                item.get("_phone", ""),
                item.get("employee_id", ""),
                item.get("department", ""),
                item.get("salary", 0)
            )
            faculty._person_id = item.get("_person_id")
            faculty.courses_taught = item.get("courses_taught", [])
            self.faculty.append(faculty)

        self.courses = {}
        for cid, item in data.get("courses", {}).items():
            course = Course(
                item.get("course_id", cid),
                item.get("course_name", ""),
                item.get("credits", 0)
            )
            employee_id = item.get("faculty_assigned")
            if employee_id:
                course.faculty_assigned = self.find_faculty(employee_id)
            course.students = [
                student for student_id in item.get("students", [])
                if (student := self.find_student(student_id))
            ]
            self.courses[cid] = course

        library_data = data.get("library", {})
        self.library = Library()
        self.library.books = library_data.get("books", [])
        self.library.issued_books = library_data.get("issued_books", {})

        self.fee_records = {}
        for sid, item in data.get("fee_records", {}).items():
            fee = Fee(item.get("student_id", sid), item.get("total_fee", 0))
            fee.paid_fee = item.get("paid_fee", 0)
            fee.balance_fee = item.get("balance_fee", fee.total_fee - fee.paid_fee)
            self.fee_records[sid] = fee

        self.attendance_records = {}
        for key, item in data.get("attendance_records", {}).items():
            record = Attendance(item.get("student_id", ""), item.get("course_id", ""))
            record.total_classes = item.get("total_classes", 0)
            record.present_classes = item.get("present_classes", 0)
            self.attendance_records[key] = record

        self.result_records = {}
        for sid, item in data.get("result_records", {}).items():
            result = Result(item.get("student_id", sid))
            result.subject_marks = item.get("marks", {})
            result.grade = item.get("grades", {})
            result.cgpa = item.get("cgpa", 0.0)
            self.result_records[sid] = result

        return data
