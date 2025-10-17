from employee import Employee

class OrganizationManager:
    def __init__(self):
        self.president = None
        self.all_names = set()      # Keeps names unique
        self.employee_lookup = {}   # Dict for name to Employee object


    # ----- Helper Methods -----

    def _find_employee(self, name: str):
        # Utility to quickly find an employee object by name.
        return self.employee_lookup.get(name)
        
    def _is_manager_of(self, manager, employee):
        # Checks if the manager is in the employee's hierarchy (up the tree).
        pass


    # ----- Main Methods -----

    def initialize_president(self, name: str) -> bool:
        # Checks if president already exists
        if self.president is not None: return False
        
        president = Employee(name=name, role="President", boss=None)
        self.president = president
        self.all_names.add(name)
        self.employee_lookup[name] = president
        print(f"Success: Initialized President {name}.")
        return True

    def hire_employee(self, hiring_manager_name: str, new_employee_name: str, new_role: str):
        # Hires a new employee under a specific manager (Requirement 3).
        pass

    def fire_employee(self, firing_manager_name: str, target_employee_name: str):
        # Removes an employee, leaving a vacancy. Firing manager must be in target's hierarchy (Requirement 4).
        pass

    def employee_quits(self, employee_name: str):
        # An employee quits (Requirement 5). Vacancy remains. President cannot quit.
        pass

    def layoff_employee(self, manager_name: str, target_employee_name: str):
        # Lays off an employee. Attempts to transfer them to the closest comparable opening (Requirement 6).
        pass

    def transfer_employee(self, initiator_name: str, employee_name: str, destination_manager_name: str):
        # Transfers an employee to the same level. Initiator must manage both spots, and destination must be vacant (Requirement 7).
        pass

    def promote_employee(self, receiving_manager_name: str, target_employee_name: str):
        # Promotes an employee one level to a vacancy under a different organization (Requirement 8).
        pass

    def load_organization_from_file(self, filepath: str):
        # Reads in the initial organization structure from a file (Requirement 9).
        pass

    def display_organization(self):
        # Displays the current organization hierarchy, hiding specific vacancies (Requirement 11).
        pass
