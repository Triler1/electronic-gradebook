from src.student import Student

class GradeBook:
    def __init__(self):
        self.students = {}

    def add_student(self, student_id, name, score=0):
        if student_id in self.students:
            raise ValueError("Студент с таким id уже существует")
        self.students[student_id] = Student(student_id, name, score)

    def update_score(self, student_id, score):
        if student_id not in self.students:
            raise ValueError("Студент с таким id не найден")
        self.students[student_id].score = score

    def get_score_by_id(self, student_id):
        if student_id not in self.students:
            raise ValueError("Студент с таким id не найден")
        return self.students[student_id].score

    def get_score_by_name(self, name):
        for student in self.students.values():
            if student.name == name:
                return student.score

    def show_all_students(self):
        return list(self.students.values())

    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError("Студент с таким id не найден")
        del self.students[student_id]