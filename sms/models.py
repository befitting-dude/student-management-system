from dataclasses import dataclass, asdict


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    course: str
    marks: float

    def to_dict(self) -> dict:
        """Convert the dataclass into a serializable dictionary."""
        return asdict(self)
