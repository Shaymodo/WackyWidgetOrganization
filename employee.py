from abc import ABC
from re import S

ROLE_CAPACITY = {
    "President": 2,
    "Vice President": 3,
    "Supervisor": 5,
    "Worker": 0
}

class OrganizationSpot(ABC):
    def is_vacant(self):
        return isinstance(self, Vacancy)

class Employee(OrganizationSpot):
    def __init__(self, name: str, role: str, boss=None):
        self.name = name                # Unique name, Dont know if just first/last or full name yet
        self.role = role                # Position in the company
        self.boss = boss                # Reference to Employee directly above
        self.reports = []               # List of Employees directly below
        self.max_reports = ROLE_CAPACITY.get(role, 0) # Maximum number of direct reports

    def promote(self):
        if self.role == "Worker":
            self.role = "Supervisor"
        elif self.role == "Supervisor":
            self.role = "Vice President"
        self.max_reports = ROLE_CAPACITY.get(self.role, 0)

class Vacancy(OrganizationSpot):
    def __init__(self, role: str, boss=None):
        self.role = role        # Position in the company
        self.boss = boss        # Reference to Employee directly above
        self.reports = []       # List of Employees directly below
        self.max_reports = ROLE_CAPACITY.get(role, 0) # Maximum number of direct reports