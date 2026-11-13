import json
import os

from student import Student


class StudentManager:
    """Stores students and handles add, find, remove, save and load."""

    def __init__(self, filename="students.json"):
        self._filename = filename
        self._students = {}
        self.load()

    def add_student(self, student: Student):
        if student.admission_number in self._students:
            raise ValueError("A student with that admission number already exists.")
        self._students[student.admission_number] = student
        self.save()

    def find_student(self, admission_number):
        return self._students.get(admission_number.strip())

    def remove_student(self, admission_number):
        if admission_number.strip() not in self._students:
            raise KeyError("Student not found.")
        del self._students[admission_number.strip()]
        self.save()

    def all_students(self):
        return sorted(self._students.values(), key=lambda s: s.admission_number)

    def search_by_name(self, text):
        text = text.lower()
        return [s for s in self.all_students() if text in s.name.lower()]

    def class_average(self):
        students = self.all_students()
        if not students:
            return 0.0
        return round(sum(s.average_mark for s in students) / len(students), 2)

    # Persistence
    def save(self):
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self._students.values()], f, indent=2)

    def load(self):
        if not os.path.exists(self._filename):
            return
        try:
            with open(self._filename, encoding="utf-8") as f:
                for item in json.load(f):
                    s = Student.from_dict(item)
                    self._students[s.admission_number] = s
        except (json.JSONDecodeError, KeyError, ValueError):
            print("Warning: could not read saved data. Starting empty.")