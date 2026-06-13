class Attendance:
    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id
        self.total_classes = 0
        self.present_classes = 0

    def mark_attendance(self, present=True):
        self.total_classes += 1
        if present:
            self.present_classes += 1

    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0.0
        return round((self.present_classes / self.total_classes) * 100, 2)

    def __str__(self):
        return f"Attendance(Student: {self.student_id}, Course: {self.course_id}, {self.attendance_percentage()}%)"

    def __repr__(self):
        return f"Attendance(student_id={self.student_id}, course_id={self.course_id}, total={self.total_classes}, present={self.present_classes})"
