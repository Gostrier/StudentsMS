class GradeSystem:
    GRADE_POINTS = {"A": 5.0, "B": 4.0, "C": 3.0, "D": 2.0, "F": 0.0}

    @classmethod
    def get_grade_point(cls, grade: str) -> float:
        grade = grade.strip().upper()
        if grade not in cls.GRADE_POINTS:
            raise ValueError(f"Invalid grade: {grade}")
        return cls.GRADE_POINTS[grade]

    @classmethod
    def calculate_gpa(cls, grades: list[str]) -> float:
        if not grades:
            return 0.0
        total = sum(cls.get_grade_point(g) for g in grades)
        return round(total / len(grades), 2)

    @staticmethod
    def mark_to_grade(mark: float) -> str:
        if mark >= 70:
            return "A"
        if mark >= 60:
            return "B"
        if mark >= 50:
            return "C"
        if mark >= 40:
            return "D"
        return "F"