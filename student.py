class Student:
    """Combines all student data into one unit and validates it."""

    def __init__(self, admission_number, name, programme,
                 year_of_study, average_mark=0.0, registered=False):
        self._admission_number = self._require_text(admission_number, "Admission number")
        self.name = name
        self.programme = programme
        self.year_of_study = year_of_study
        self.average_mark = average_mark
        self._registered = bool(registered)

    @staticmethod
    def _require_text(value, label):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{label} cannot be empty.")
        return value

    # Read-only admission number
    @property
    def admission_number(self):
        return self._admission_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._require_text(value, "Name")

    @property
    def programme(self):
        return self._programme

    @programme.setter
    def programme(self, value):
        self._programme = self._require_text(value, "Programme")

    @property
    def year_of_study(self):
        return self._year_of_study

    @year_of_study.setter
    def year_of_study(self, value):
        value = int(value)
        if not 1 <= value <= 6:
            raise ValueError("Year of study must be between 1 and 6.")
        self._year_of_study = value

    @property
    def average_mark(self):
        return self._average_mark

    @average_mark.setter
    def average_mark(self, value):
        value = float(value)
        if not 0 <= value <= 100:
            raise ValueError("Average mark must be between 0 and 100.")
        self._average_mark = value

    @property
    def registered(self):
        return self._registered

    # Behaviour
    def register(self):
        self._registered = True

    def deregister(self):
        self._registered = False

    def to_dict(self):
        return {
            "admission_number": self._admission_number,
            "name": self._name,
            "programme": self._programme,
            "year_of_study": self._year_of_study,
            "average_mark": self._average_mark,
            "registered": self._registered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["admission_number"], data["name"], data["programme"],
            data["year_of_study"], data["average_mark"], data["registered"],
        )

    def __str__(self):
        status = "Registered" if self._registered else "Not registered"
        return (f"{self._admission_number:<14} {self._name:<22} "
                f"{self._programme:<20} Yr {self._year_of_study}  "
                f"{self._average_mark:>5.1f}  {status}")