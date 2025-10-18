from tkinter import N
from employee import Employee, Vacancy

# TODO:
# Ensure Vacancy objects do not prevent hiring in their spots
# President transfers employee to themselves giving wrong error message
# Check if a Vacancy object has no reports, delete Vacancy object if so
# Layoff implementation
# Read organization from file implementation
# Add checks for inputting president name at start of program


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
        # Determines the role of an employee based on the manager's role.
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
        while current_boss != None:
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

    def _remove_employee(self, employee):
        self.all_names.remove(employee)
        del self.employee_lookup[employee]

        # If the target employee has no reports
        if len(employee.reports) == 0:
            employee.boss.reports.remove(employee)
            print(f"{employee.name} has been removed from the company.")

        # If the target employee has reports, leave a vacancy
        elif len(employee.reports) > 0:
            self._replace_employee_with_vacancy(employee)
            print(f"{employee.name} has been removed from the company. Vacancy remains.")

    def _move_employee(self, employee, new_boss, replacement_index):
        employee.boss.reports.remove(employee)
        if replacement_index == -1:
            new_boss.reports.append(employee)
        else:
            new_boss.reports[replacement_index] = employee
        employee.boss = new_boss

    def _has_spots(self, manager):
        # Checks if a manager has availability for new reports. Returns True if open spot, index of Vacancy if found, False otherwise.
        if len(manager.reports) < manager.max_reports:
            return True
        # Check for Vacancy objects
        index = self._check_vancancy_objects(manager)
        if index != -1:
            return index
        return False

    def _check_vancancy_objects(self, manager):
        # Checks for Vacancy objects under a manager and returns the first index if found, -1 otherwise.
        for index, report in enumerate(manager.reports):
            if isinstance(report, Vacancy):
                return index
        return -1

    def _search_vice_presidents(self, president, invalid_index):
        # Searches through VPs under the President for an opening. invalid_index is the index of the VP to skip. invalid_index = -1 means no skip.
        # Has empty spot
        if self._has_spots(president):
            return -1, president
        # Has Vacancy object
        elif self._has_spots(president) != False:
            return self._check_vancancy_objects(president), president

        # No Vice President openings found
        return None, None

    def _search_supervisors(self, VP, invalid_index):
        # Searches through Supervisors under a VP for an opening. invalid_index is the index of the Supervisor to skip. invalid_index = -1 means no skip.
        # Has empty spot
        if self._has_spots(VP):
            return -1, VP
        # Has Vacancy object
        elif self._has_spots(VP) != False:
            return self._check_vancancy_objects(VP), VP

        return None, None

    def _search_workers(self, supervisor, invalid_index):
        # Searches through Workers under a Supervisor for an opening. invalid_index is the index of the Worker to skip. invalid_index = -1 means no skip.
        pass

    def _find_opening(self, current_manager, role, current_index):
        # Finds the closest comparable opening, returns report index and new boss object
        # If there is another VP position available under President, return that index and President object
        if role == "Vice President":
            new_index, new_boss = self._search_vice_presidents(current_manager.boss, current_index)
        elif role == "Supervisor":
            new_index, new_boss = self._search_supervisors(current_manager.boss, current_index)
        elif role == "Worker":
            new_index, new_boss = self._search_workers(current_manager.boss, current_index)

        # If the found opening does not match the role, return None -------- FIX THIS LATER
        if role != self._determine_valid_role(new_boss):
            return None, None
        return new_index, new_boss

    # ----- Main Methods -----

    def initialize_president(self, name: str):
        # Checks if president already exists, should never happen
        if self.president != None: return False
        
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
        if not self._has_spots(hiring_manager):
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
        self._remove_employee(target_employee)
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
        self._remove_employee(self._find_employee(employee_name))
        return


    # FINISH THIS ----------------------------------------------------------------------
    def layoff_employee(self, manager_name: str, target_employee_name: str):
        # Lays off an employee. Attempts to transfer them to the closest comparable opening (Requirement 6).
        # Cannot lay off President
        if target_employee_name == self.president.name:
            print("Error: Cannot lay off the President.")
            return

        # Checks if names exist
        if manager_name not in self.all_names:
            print(f"Error: Manager {manager_name} does not exist.")
            return
        if target_employee_name not in self.all_names:
            print(f"Error: Employee name {target_employee_name} does not exist.")
            return

        manager = self._find_employee(manager_name)
        target_employee = self._find_employee(target_employee_name)

        # Checks if manager is in target employee's hierarchy
        if not self._is_manager_of(manager, target_employee):
            print(f"Error: {manager_name} is not in the hierarchy of {target_employee_name}.")
            return

        index, new_boss = self._find_opening(target_employee.boss, target_employee.role, target_employee.boss.reports.index(target_employee))

        # No opening found, remove employee
        if index == None:
            self._remove_employee(target_employee)
            return

        # Empty spot or Vacancy found, move employee to new location
        else:
            self._move_employee(target_employee, new_boss, index)


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

        initiator = self._find_employee(initiator_name)

        # Checks if initiator is President or VP
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
        if not self._has_spots(destination_manager):
            print(f"Error: Destination manager {destination_manager_name} has reached maximum direct reports.")
            return

        replacement_index = self._check_vancancy_objects(destination_manager)

        # If everything is valid, perform the transfer
        self._move_employee(employee, destination_manager, replacement_index)
        print(f"Successfully transferred {employee_name} to {destination_manager_name}.")

        return


    def promote_employee(self, receiving_manager_name: str, target_employee_name: str):
        # Promotes an employee one level to a vacancy under a different organization (Requirement 8).
        # Checks if names exist
        if receiving_manager_name not in self.all_names:
            print(f"Error: Receiving manager {receiving_manager_name} does not exist.")
            return
        if target_employee_name not in self.all_names:
            print(f"Error: Employee name {target_employee_name} does not exist.")
            return

        receiving_manager = self._find_employee(receiving_manager_name)
        target_employee = self._find_employee(target_employee_name)

        # Checks if target employee can be promoted
        if target_employee.role == "Vice President" or target_employee.role == "President":
            print(f"Error: {target_employee_name} cannot be promoted further.")
            return

        # Checks if receiving manager can promote
        if receiving_manager.role == "Worker" or receiving_manager.role == "Supervisor":
            print(f"Error: {receiving_manager_name} cannot promote employees.")
            return

        # President cannot promote Workers
        if receiving_manager.role == "President" and target_employee.role == "Worker":
            print(f"Error: Promotions can only be one level.")
            return

        # Checks if there is an open spot
        if not self._has_spots(receiving_manager):
            print(f"Error: Receiving manager {receiving_manager_name} has reached maximum direct reports.")
            return

        # Checks if target employee is not becoming boss of their current peers
        for index, report in enumerate(receiving_manager.reports):
            if isinstance(report, Vacancy) and target_employee not in report.reports:
                if target_employee.role != "Worker":
                    self._replace_employee_with_vacancy(target_employee)
                else:
                    target_employee.boss.reports.remove(target_employee)
                target_employee.boss = receiving_manager
                target_employee.reports = receiving_manager.reports[index].reports
                receiving_manager.reports[index] = target_employee
                target_employee.promote()
                print(f"aaaSuccessfully promoted {target_employee_name} under {receiving_manager_name}.")
                return

        # No Vacancy object found, normal addition
        target_employee.boss.reports.remove(target_employee)
        target_employee.boss = receiving_manager
        receiving_manager.reports.append(target_employee)
        target_employee.promote()

        print(f"bbbSuccessfully promoted {target_employee_name} under {receiving_manager_name}.")
        return


    # Finish this ----------------------------------------------------------------------
    def load_organization_from_file(self, filepath: str):
        # Reads in the initial organization structure from a file (Requirement 9).
        # Checks if file exists
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            return
        # Process each line
        for line in lines:
            # Need to decide on file format first
            pass
        return


    def display_organization(self):
        # Displays the current organization hierarchy (Requirement 11).
        if self.president is None:
            print("Organization is empty.")

        print(f"President: {self.president.name}")
        self._display_loop(self.president, 1)
        return