class Result:
    def __init__(self, student_id):
        self.student_id = student_id
        self.subject_marks = {}  # subject: marks
        self.grade = {}
        self.cgpa = 0.0

    def enter_marks(self, subject, marks):
        if marks < 0 or marks > 100:
            raise ValueError("Invalid marks: must be between 0 and 100.")
        self.subject_marks[subject] = marks

    def calculate_grade(self, subject):
        marks = self.subject_marks.get(subject, None)
        if marks is None:
            return None
        if marks >= 90:
            grade = "A+"
        elif marks >= 80:
            grade = "A"
        elif marks >= 70:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 50:
            grade = "D"
        else:
            grade = "F"
        self.grade[subject] = grade
        return grade

    def calculate_cgpa(self):
        if not self.subject_marks:
            return 0.0
        total_points = 0
        for subject, marks in self.subject_marks.items():
            self.calculate_grade(subject)
            total_points += marks / 10  # simple conversion: marks/10 = grade points
        self.cgpa = round(total_points / len(self.subject_marks), 2)
        return self.cgpa

    def generate_result(self):
        return {
            "student_id": self.student_id,
            "marks": self.subject_marks,
            "grades": self.grade,
            "cgpa": self.cgpa
        }

    def __str__(self):
        return f"Result(Student: {self.student_id}, CGPA: {self.cgpa})"

    def __repr__(self):
        return f"Result(student_id={self.student_id}, subjects={list(self.subject_marks.keys())})"
