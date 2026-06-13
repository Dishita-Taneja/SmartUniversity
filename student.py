from person import Person

class Student(Person):
    def __init__(self, name, email, phone, roll_no, department, semester):
        super().__init__(name, email, phone)
        self.roll_no = roll_no
        self.department = department
        self.semester = semester
        self.registered_courses = []
        self.results = {}  # subject: grade points

    def generate_id(self):
        self._person_id = f"S-{self.roll_no}"
        return self._person_id

    def display_details(self):
        return f"Student: {self._name}, Roll: {self.roll_no}, Dept: {self.department}, Semester: {self.semester}"

    def register_course(self, course_id):
        if course_id not in self.registered_courses:
            self.registered_courses.append(course_id)
        else:
            raise ValueError("Duplicate registration: already registered in this course.")

    def drop_course(self, course_id):
        if course_id in self.registered_courses:
            self.registered_courses.remove(course_id)
        else:
            raise ValueError("Course not found in registered list.")

    def view_result(self):
        return self.results

    def calculate_cgpa(self):
        if not self.results:
            return 0.0
        return round(sum(self.results.values()) / len(self.results), 2)

    def __str__(self):
        return f"Student {self._name} (Roll: {self.roll_no})"

    def __repr__(self):
        return f"Student(name={self._name}, roll_no={self.roll_no}, dept={self.department}, sem={self.semester})"
