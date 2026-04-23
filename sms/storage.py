import csv
import json
from pathlib import Path

from sms.models import Student


class FileStorage:
    """Persist student records in both JSON and CSV formats."""

    headers = ["student_id", "name", "age", "course", "marks"]

    def __init__(self, json_file: Path, csv_file: Path) -> None:
        self.json_file = json_file
        self.csv_file = csv_file
        self._ensure_files()

    def _ensure_files(self) -> None:
        self.json_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.json_file.exists():
            self.json_file.write_text("[]", encoding="utf-8")

        if not self.csv_file.exists():
            with self.csv_file.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()

    def load_students(self) -> list[Student]:
        try:
            raw_data = json.loads(self.json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            raw_data = []

        students = []
        for item in raw_data:
            students.append(
                Student(
                    student_id=item["student_id"],
                    name=item["name"],
                    age=int(item["age"]),
                    course=item["course"],
                    marks=float(item["marks"]),
                )
            )
        return students

    def save_students(self, students: list[Student]) -> None:
        serialized = [student.to_dict() for student in students]
        self.json_file.write_text(json.dumps(serialized, indent=4), encoding="utf-8")

        with self.csv_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(serialized)
