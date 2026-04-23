from sms.exceptions import ValidationError


def validate_student_id(student_id: str) -> str:
    student_id = student_id.strip().upper()
    if not student_id:
        raise ValidationError("Student ID cannot be empty.")
    return student_id


def validate_name(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValidationError("Name cannot be empty.")
    if any(char.isdigit() for char in name):
        raise ValidationError("Name cannot contain numbers.")
    return name.title()


def validate_age(age_text: str) -> int:
    try:
        age = int(age_text)
    except ValueError as exc:
        raise ValidationError("Age must be a valid integer.") from exc

    if age < 3 or age > 100:
        raise ValidationError("Age must be between 3 and 100.")
    return age


def validate_course(course: str) -> str:
    course = course.strip()
    if not course:
        raise ValidationError("Course cannot be empty.")
    return course.title()


def validate_marks(marks_text: str) -> float:
    try:
        marks = float(marks_text)
    except ValueError as exc:
        raise ValidationError("Marks must be a valid number.") from exc

    if marks < 0 or marks > 100:
        raise ValidationError("Marks must be between 0 and 100.")
    return round(marks, 2)
