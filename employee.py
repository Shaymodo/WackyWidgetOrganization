ROLE_CAPACITY = {
    "President": 2,
    "Vice President": 3,
    "Supervisor": 5,
    "Worker": 0
}

class Employee:
    def __init__(self, name: str, role: str, boss=None):
        self.name = name        # Unique name, Dont know if just first/last or full name yet
        self.role = role        # Position in the company
        self.boss = boss        # Reference to Employee directly above
        self.reports = []       # List of Employees directly below
        self.max_reports = ROLE_CAPACITY.get(role, 0) # Maximum number of direct reports
    
    def get_level(self):
        if self.role == "President": return 4
        if self.role == "Vice President": return 3
        if self.role == "Supervisor": return 2
        if self.role == "Worker": return 1
        return 0