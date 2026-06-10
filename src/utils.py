from src.student import Student

def print_student(student):
    print(f"{student.student_id}. {student.name} -> {student.score}")

def print_students(students):
    if not students:
        print("Журнал пуст")
        return
    for student in students:
        print_student(student)