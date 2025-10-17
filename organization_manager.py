from employee import Employee, Vacancy

# TODO: Ensure Vacancy objects do not prevent hiring in their spots

class OrganizationManager:
    def __init__(self):
        self.president = None
        self.all_names = set()      # Keeps names unique
        self.employee_lookup = {}   # Dict for name to Employee object


    # ----- Helper Methods -----

    def _find_employee(self, name: str):
        # Utility to quickly find an employee object by name.
        return self.employee_lookup.get(name)

    def _determine_valid_role(self, manager):
        # Determines the role of a new hire based on the manager's role.
        match manager.role:
            case "President":
                return "Vice President"
            case "Vice President":
                return "Supervisor"
            case "Supervisor":
                return "Worker"
        
    def _is_manager_of(self, manager, employee):
        # Checks if the manager is in the employee's hierarchy (up the tree).
        current_boss = employee.boss
        while current_boss is not None:
            if current_boss is manager:
                return True
            current_boss = current_boss.boss
        return False

    def _display_loop(self, current_spot, depth):
        # Recursive function to display the organization structure.
        indent = "\t" * depth
        for report in current_spot.reports:
            if isinstance(report, Vacancy):
                print(f"{indent}VACANCY: {report.role}")
            else:
                print(f"{indent}{report.role}: {report.name}")
            self._display_loop(report, depth + 1)

    def _replace_employee_with_vacancy(self, employee):
        # Replaces an employee with a vacancy, transferring reports to the vacancy.
        vacancy = Vacancy(role=employee.role, boss=employee.boss)
        employee_index = employee.boss.reports.index(employee)
        employee.boss.reports[employee_index] = vacancy
        # Assign the reports to the vacancy
        for report in employee.reports:
            report.boss = vacancy
            vacancy.reports.append(report)

    # ----- Main Methods -----

    def initialize_president(self, name: str):
        # Checks if president already exists, should never happen
        if self.president is not None: return False
        
        president = Employee(name=name, role="President", boss=None)
        self.president = president
        self.all_names.add(name)
        self.employee_lookup[name] = president
        print(f"Success: Initialized President {name}.")
        return True

    def hire_employee(self, hiring_manager_name: str, new_employee_name: str):
        # Hires a new employee under a specific manager (Requirement 3).
        # Checks if names exist
        if hiring_manager_name not in self.all_names:
            print(f"Error: Hiring manager {hiring_manager_name} does not exist.")
            return
        if new_employee_name in self.all_names:
            print(f"Error: Employee name {new_employee_name} already exists.")
            return

        hiring_manager = self._find_employee(hiring_manager_name)
        # Checks if hiring manager can hire
        if hiring_manager.role == "Worker":
            print(f"Error: A worker cannot hire employees.")
            return
        # Checks if there is an open spot
        if len(hiring_manager.reports) >= hiring_manager.max_reports:
            print(f"Error: Hiring manager {hiring_manager_name} has reached maximum direct reports.")
            return

        # If everything is valid, create and add the new employee
        new_employee = Employee(name=new_employee_name, role=self._determine_valid_role(hiring_manager), boss=hiring_manager)
        hiring_manager.reports.append(new_employee)
        self.all_names.add(new_employee_name)
        self.employee_lookup[new_employee_name] = new_employee

        print(f"Successfully hired {new_employee_name} under {hiring_manager_name}.")

        return

    def fire_employee(self, firing_manager_name: str, target_employee_name: str):
        # Removes an employee, leaving a vacancy. Firing manager must be in target's hierarchy (Requirement 4).
        # Checks if names exist
        if target_employee_name == self.president.name:
            print("Error: Cannot fire the President.")
            return
        if firing_manager_name not in self.all_names:
            print(f"Error: Firing manager {firing_manager_name} does not exist.")
            return
        if target_employee_name not in self.all_names:
            print(f"Error: Employee name {target_employee_name} does not exist.")
            return

        firing_manager = self._find_employee(firing_manager_name)
        target_employee = self._find_employee(target_employee_name)
        # Checks if firing manager is in target employee's hierarchy
        if not self._is_manager_of(firing_manager, target_employee):
            print(f"Error: {firing_manager_name} is not in the hierarchy of {target_employee_name}.")
            return

        # If everything is valid, remove the employee
        self.all_names.remove(target_employee_name)
        del self.employee_lookup[target_employee_name]

        # If the target employee has no reports
        if len(target_employee.reports) == 0:
            target_employee.boss.reports.remove(target_employee)
            print(f"Successfully fired {target_employee_name}.")

        # If the target employee has reports, leave a vacancy
        elif len(target_employee.reports) > 0:
            self._replace_employee_with_vacancy(target_employee)
            print(f"Successfully fired {target_employee_name}. Vacancy remains.")

        return

    def employee_quits(self, employee_name: str):
        # An employee quits. Vacancy remains. President cannot quit. (Requirement 5)
        # Checks if names exist
        if employee_name == self.president.name:
            print("Error: President cannot quit.")
            return
        if employee_name not in self.all_names:
            print(f"Error: Employee name {employee_name} does not exist.")
            return

        # Remove employee
        self._replace_employee_with_vacancy(self._find_employee(employee_name))
        print(f"{employee_name} has quit. Vacancy remains.")
        return

    def layoff_employee(self, manager_name: str, target_employee_name: str):
        # Lays off an employee. Attempts to transfer them to the closest comparable opening (Requirement 6).
        return

    def transfer_employee(self, initiator_name: str, employee_name: str, destination_manager_name: str):
        # Transfers an employee to the same level. Initiator must manage both spots, and destination must be vacant (Requirement 7).
        # Checks if names all exist
        if initiator_name not in self.all_names:
            print(f"Error: Initiator {initiator_name} does not exist.")
            return
        if employee_name not in self.all_names:
            print(f"Error: Employee name {employee_name} does not exist.")
            return
        if destination_manager_name not in self.all_names:
            print(f"Error: Destination manager {destination_manager_name} does not exist.")
            return
        # Checks if initiator is President or VP
        initiator = self._find_employee(initiator_name)
        if initiator.role not in ["President", "Vice President"]:
            print(f"Error: Initiator {initiator_name} does not have permission to transfer employees.")
            return
        # Checks if initiator manages employee getting transferred
        employee = self._find_employee(employee_name)
        if not self._is_manager_of(initiator, employee):
            print(f"Error: {initiator_name} does not manage {employee_name}.")
            return
        # Checks if initiator manages destination manager
        destination_manager = self._find_employee(destination_manager_name)
        if not self._is_manager_of(initiator, destination_manager):
            print(f"Error: {initiator_name} does not manage {destination_manager_name}.")
            return
        # Checks if roles match
        if employee.role != self._determine_valid_role(destination_manager):
            print(f"Error: Employee {employee_name} cannot be transferred to {destination_manager_name} due to role mismatch.")
            return
        # Checks if a spot is available
        if len(destination_manager.reports) >= destination_manager.max_reports:
            print(f"Error: Destination manager {destination_manager_name} has no vacancies.")
            return

        # If everything is valid, perform the transfer
        employee.boss.reports.remove(employee)
        destination_manager.reports.append(employee)
        employee.boss = destination_manager
        print(f"Successfully transferred {employee_name} to {destination_manager_name}.")

        return

    def promote_employee(self, receiving_manager_name: str, target_employee_name: str):
        # Promotes an employee one level to a vacancy under a different organization (Requirement 8).
        return

    def load_organization_from_file(self, filepath: str):
        # Reads in the initial organization structure from a file (Requirement 9).
        return

    def display_organization(self):
        # Displays the current organization hierarchy (Requirement 11).
        if self.president is None:
            print("Organization is empty.")

        print(f"President: {self.president.name}")
        self._display_loop(self.president, 1)
        return