from grade_system import GradeSystem
from student import Student
from student_manager import StudentManager

MENU = """
===== UNIVERSITY STUDENT MANAGEMENT SYSTEM =====
1. Add student
2. View all students
3. Find student by admission number
4. Search student by name
5. Register student
6. Deregister student
7. Update average mark
8. Remove student
9. Class average
10. GPA calculator
0. Exit
"""


def add_student(mgr):
    try:
        s = Student(
            input("Admission number: "),
            input("Name: "),
            input("Programme: "),
            input("Year of study (1-6): "),
            input("Average mark (0-100): "),
        )
        mgr.add_student(s)
        print("Student added.")
    except ValueError as e:
        print(f"Error: {e}")


def view_all(mgr):
    students = mgr.all_students()
    if not students:
        print("No students yet.")
        return
    for s in students:
        print(s)


def find_student(mgr):
    s = mgr.find_student(input("Admission number: "))
    print(s if s else "Student not found.")


def search_name(mgr):
    results = mgr.search_by_name(input("Name contains: "))
    if not results:
        print("No matches.")
    for s in results:
        print(s)


def change_registration(mgr, register=True):
    s = mgr.find_student(input("Admission number: "))
    if not s:
        print("Student not found.")
        return
    s.register() if register else s.deregister()
    mgr.save()
    print("Registration updated.")


def update_mark(mgr):
    s = mgr.find_student(input("Admission number: "))
    if not s:
        print("Student not found.")
        return
    try:
        s.average_mark = input("New average mark: ")
        mgr.save()
        print("Mark updated.")
    except ValueError as e:
        print(f"Error: {e}")


def remove_student(mgr):
    try:
        mgr.remove_student(input("Admission number: "))
        print("Student removed.")
    except KeyError as e:
        print(e)


def gpa_calculator():
    raw = input("Enter grades separated by spaces (e.g. A B C): ").split()
    try:
        print("GPA:", GradeSystem.calculate_gpa(raw))
    except ValueError as e:
        print(f"Error: {e}")


def main():
    mgr = StudentManager()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_student(mgr)
        elif choice == "2":
            view_all(mgr)
        elif choice == "3":
            find_student(mgr)
        elif choice == "4":
            search_name(mgr)
        elif choice == "5":
            change_registration(mgr, True)
        elif choice == "6":
            change_registration(mgr, False)
        elif choice == "7":
            update_mark(mgr)
        elif choice == "8":
            remove_student(mgr)
        elif choice == "9":
            print("Class average:", mgr.class_average())
        elif choice == "10":
            gpa_calculator()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()