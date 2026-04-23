from sms.exceptions import StudentNotFoundError, ValidationError
from sms.models import Student
from sms.storage import FileStorage
from sms.utils import (
    validate_age,
    validate_course,
    validate_marks,
    validate_name,
    validate_student_id,
)


class StudentService:
    """Business logic for managing student records."""

    def __init__(self, storage: FileStorage) -> None:
        self.storage = storage

    def list_students(self) -> list[Student]:
        return self.storage.load_students()

    def add_student(
        self, student_id: str, name: str, age_text: str, course: str, marks_text: str
    ) -> Student:
        students = self.storage.load_students()
        normalized_id = validate_student_id(student_id)

        if any(student.student_id == normalized_id for student in students):
            raise ValidationError("A student with this ID already exists.")

        student = Student(
            student_id=normalized_id,
            name=validate_name(name),
            age=validate_age(age_text),
            course=validate_course(course),
            marks=validate_marks(marks_text),
        )

        students.append(student)
        self.storage.save_students(students)
        return student

    def update_student(
        self, student_id: str, name: str, age_text: str, course: str, marks_text: str
    ) -> Student:
        students = self.storage.load_students()
        normalized_id = validate_student_id(student_id)

        for index, student in enumerate(students):
            if student.student_id == normalized_id:
                updated_student = Student(
                    student_id=normalized_id,
                    name=validate_name(name),
                    age=validate_age(age_text),
                    course=validate_course(course),
                    marks=validate_marks(marks_text),
                )
                students[index] = updated_student
                self.storage.save_students(students)
                return updated_student

        raise StudentNotFoundError("Student ID not found.")

    def delete_student(self, student_id: str) -> None:
        students = self.storage.load_students()
        normalized_id = validate_student_id(student_id)
        filtered_students = [
            student for student in students if student.student_id != normalized_id
        ]

        if len(filtered_students) == len(students):
            raise StudentNotFoundError("Student ID not found.")

        self.storage.save_students(filtered_students)

    def search_students(self, keyword: str) -> list[Student]:
        keyword = keyword.strip().lower()
        if not keyword:
            raise ValidationError("Search keyword cannot be empty.")

        students = self.storage.load_students()
        return [
            student
            for student in students
            if keyword in student.student_id.lower()
            or keyword in student.name.lower()
            or keyword in student.course.lower()
        ]

    def sort_students(self, sort_by: str) -> list[Student]:
        students = self.storage.load_students()

        if sort_by == "name":
            return sorted(students, key=lambda student: student.name.lower())
        if sort_by == "marks":
            return sorted(students, key=lambda student: student.marks, reverse=True)

        raise ValidationError("Sort option must be 'name' or 'marks'.")
