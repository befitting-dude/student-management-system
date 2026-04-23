from statistics import mean

from sms.models import Student


class ReportGenerator:
    """Generate analytics from student records."""

    @staticmethod
    def generate_summary(students: list[Student]) -> dict:
        if not students:
            return {
                "total_students": 0,
                "average_marks": 0,
                "topper": None,
                "passed_students": 0,
                "failed_students": 0,
            }

        topper = max(students, key=lambda student: student.marks)
        passed_students = sum(student.marks >= 40 for student in students)
        failed_students = len(students) - passed_students

        return {
            "total_students": len(students),
            "average_marks": round(mean(student.marks for student in students), 2),
            "topper": topper,
            "passed_students": passed_students,
            "failed_students": failed_students,
        }
