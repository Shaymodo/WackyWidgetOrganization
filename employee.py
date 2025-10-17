from abc import ABC
from re import S

ROLE_CAPACITY = {
    "President": 2,
    "Vice President": 3,
    "Supervisor": 5,
    "Worker": 0
}

class OrganizationSpot(ABC):
    def get_level(self):
        match self.role:
            case "President":
                return 4
            case "Vice President":
                return 3
            case "Supervisor":
                return 2
            case "Worker":
                return 1
        return 0
    def is_vacant(self):
        return isinstance(self, Vacancy)

class Employee(OrganizationSpot):
    def __init__(self, name: str, role: str, boss=None):
        self.name = name                # Unique name, Dont know if just first/last or full name yet
        self.role = role                # Position in the company
        self.boss = boss                # Reference to Employee directly above
        self.reports = []               # List of Employees directly below
        self.max_reports = ROLE_CAPACITY.get(role, 0) # Maximum number of direct reports

class Vacancy(OrganizationSpot):
    def __init__(self, role: str, boss=None):
        self.role = role        # Position in the company
        self.boss = boss        # Reference to Employee directly above
        self.reports = []       # List of Employees directly below
        self.max_reports = ROLE_CAPACITY.get(role, 0) # Maximum number of direct reports