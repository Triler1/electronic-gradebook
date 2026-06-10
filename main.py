from src.gradebook import GradeBook
from src.utils import *

def main():
    journal = GradeBook()
    journal.add_student(1, "Ivan", 78)
    journal.add_student(2, "Anna", 92)
    journal.add_student(3, "Maria", 85)
    print("Все студенты:")
    print_students(journal.show_all_students())
    print()
    print("Балл Anna:")
    print(journal.get_score_by_name("Anna"))
    print()
    print("Удаляем студента Maria:")
    journal.delete_student(3)
    print_students(journal.show_all_students())

if __name__ == "__main__":
    main()