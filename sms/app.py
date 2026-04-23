from getpass import getpass
from pathlib import Path

from sms.auth import AdminAuth
from sms.exceptions import AuthenticationError, StudentManagementError
from sms.reports import ReportGenerator
from sms.service import StudentService
from sms.storage import FileStorage


class StudentManagementApp:
    """CLI application for student record management."""

    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / "data"
        self.service = StudentService(
            FileStorage(
                json_file=data_dir / "students.json",
                csv_file=data_dir / "students.csv",
            )
        )
        self.auth = AdminAuth(data_dir / "admin.json")

    def run(self) -> None:
        print("\nStudent Management System")
        print("-" * 28)

        if not self._authenticate():
            return

        while True:
            self._show_menu()
            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self._add_student()
                elif choice == "2":
                    self._update_student()
                elif choice == "3":
                    self._delete_student()
                elif choice == "4":
                    self._search_students()
                elif choice == "5":
                    self._display_students(self.service.list_students())
                elif choice == "6":
                    self._sort_students()
                elif choice == "7":
                    self._show_report()
                elif choice == "8":
                    print("Exiting the system. Goodbye.")
                    break
                else:
                    print("Please enter a valid menu option.")
            except StudentManagementError as error:
                print(f"Error: {error}")
            except Exception as error:
                print(f"Unexpected error: {error}")

    def _authenticate(self) -> bool:
        for attempt in range(3):
            username = input("Admin username: ").strip()
            password = getpass("Admin password: ")

            try:
                if self.auth.login(username, password):
                    print("Login successful.\n")
                    return True
            except AuthenticationError as error:
                remaining = 2 - attempt
                print(f"{error} Attempts remaining: {remaining}")

        print("Too many failed login attempts.")
        return False

    @staticmethod
    def _show_menu() -> None:
        print("\n1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. View All Students")
        print("6. Sort Students")
        print("7. Generate Report")
        print("8. Exit")

    def _add_student(self) -> None:
        student = self.service.add_student(
            student_id=input("Enter student ID: "),
            name=input("Enter name: "),
            age_text=input("Enter age: "),
            course=input("Enter course: "),
            marks_text=input("Enter marks: "),
        )
        print(f"Student added successfully: {student.name}")

    def _update_student(self) -> None:
        student = self.service.update_student(
            student_id=input("Enter student ID to update: "),
            name=input("Enter updated name: "),
            age_text=input("Enter updated age: "),
            course=input("Enter updated course: "),
            marks_text=input("Enter updated marks: "),
        )
        print(f"Student updated successfully: {student.name}")

    def _delete_student(self) -> None:
        self.service.delete_student(input("Enter student ID to delete: "))
        print("Student deleted successfully.")

    def _search_students(self) -> None:
        students = self.service.search_students(input("Enter search keyword: "))
        self._display_students(students)

    def _sort_students(self) -> None:
        sort_by = input("Sort by 'name' or 'marks': ").strip().lower()
        students = self.service.sort_students(sort_by)
        self._display_students(students)

    def _show_report(self) -> None:
        summary = ReportGenerator.generate_summary(self.service.list_students())

        print("\nReport Summary")
        print("-" * 20)
        print(f"Total students : {summary['total_students']}")
        print(f"Average marks  : {summary['average_marks']}")
        print(f"Passed students: {summary['passed_students']}")
        print(f"Failed students: {summary['failed_students']}")

        topper = summary["topper"]
        if topper:
            print(
                f"Topper         : {topper.name} ({topper.student_id}) - {topper.marks}"
            )
        else:
            print("Topper         : No records available")

    @staticmethod
    def _display_students(students: list) -> None:
        if not students:
            print("No student records found.")
            return

        print("\n{:<12} {:<20} {:<6} {:<18} {:<8}".format(
            "Student ID", "Name", "Age", "Course", "Marks"
        ))
        print("-" * 70)
        for student in students:
            print(
                "{:<12} {:<20} {:<6} {:<18} {:<8}".format(
                    student.student_id,
                    student.name,
                    student.age,
                    student.course,
                    student.marks,
                )
            )
