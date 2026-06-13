from person import Person

class Faculty(Person):
    def __init__(self, name, email, phone, employee_id, department, salary):
        super().__init__(name, email, phone)
        self.employee_id = employee_id
        self.department = department
        self.salary = salary
        self.courses_taught = []

    def generate_id(self):
        self._person_id = f"F-{self.employee_id}"
        return self._person_id

    def display_details(self):
        return f"Faculty: {self._name}, ID: {self.employee_id}, Dept: {self.department}, Salary: {self.salary}"

    def assign_course(self, course_id):
        if course_id not in self.courses_taught:
            self.courses_taught.append(course_id)
        else:
            raise ValueError("Duplicate assignment: already teaching this course.")

    def mark_attendance(self, attendance_obj, present=True):
        attendance_obj.mark_attendance(present)

    def enter_marks(self, student, subject, marks):
        student.results[subject] = marks

    def __str__(self):
        return f"Faculty {self._name} (ID: {self.employee_id})"

    def __repr__(self):
        return f"Faculty(name={self._name}, employee_id={self.employee_id}, dept={self.department})"
