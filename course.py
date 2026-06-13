class Course:
    def __init__(self, course_id, course_name, credits):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.faculty_assigned = None
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
        else:
            raise ValueError("Student already registered in this course.")

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
        else:
            raise ValueError("Student not found in this course.")

    def assign_faculty(self, faculty):
        self.faculty_assigned = faculty

    def display_course(self):
        return f"Course: {self.course_name} (ID: {self.course_id}, Credits: {self.credits})"

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"

    def __repr__(self):
        return f"Course(course_id={self.course_id}, name={self.course_name}, credits={self.credits})"
