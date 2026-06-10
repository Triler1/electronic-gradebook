import unittest

from src.gradebook import GradeBook

class TestGradeBook(unittest.TestCase):
    def setUp(self):
        self.journal = GradeBook()
        self.journal.add_student(1, "Ivan", 78)
        self.journal.add_student(2, "Anna", 92)
        self.journal.add_student(3, "Maria", 85)

    def test_add_student(self):
        students = self.journal.show_all_students()
        self.assertEqual(len(students), 3)

    def test_update_score(self):
        self.journal.update_score(1, 90)
        self.assertEqual(self.journal.get_score_by_id(1), 90)

    def test_get_score_by_id(self):
        score = self.journal.get_score_by_id(2)
        self.assertEqual(score, 92)

    def test_get_score_by_name(self):
        score = self.journal.get_score_by_name("Maria")
        self.assertEqual(score, 85)

    def test_delete_student(self):
        self.journal.delete_student(3)
        students = self.journal.show_all_students()
        self.assertEqual(len(students), 2)
        with self.assertRaises(ValueError):
            self.journal.get_score_by_id(3)

    def test_duplicate_id_error(self):
        with self.assertRaises(ValueError):
            self.journal.add_student(1, "Petr", 70)

    def test_update_unknown_student_error(self):
        with self.assertRaises(ValueError):
            self.journal.update_score(999, 100)

if __name__ == "__main__":
    unittest.main(verbosity=2)