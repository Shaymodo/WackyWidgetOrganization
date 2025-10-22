from employee import Employee, Vacancy

# TODO:
# Check if a Vacancy object has no reports, delete Vacancy object if so. Should be done after every operation that moves or removes employees
# Layoff not properly creating Vacancy and leaving reports behind? Unsure if they should leave their reports behind or not
# Add checks for inputting president name at start of program
# Add initial question to load from file or create new organization
# Should we allow transferring an employee to a Vacancy?
# Could make large adjustment, changing empty spots to always be Vacancy objects instead of None. Could simplify some logic and improve consistency.

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
        
    def _add_employee(self, manager, new_employee_name):
        new_employee = Employee(name=new_employee_name, role=self._determine_valid_role(manager), boss=manager)
        manager.reports.append(new_employee)
        self.all_names.add(new_employee_name)
        self.employee_lookup[new_employee_name] = new_employee
        print(f"Successfully hired {new_employee_name} under {manager.name}.")
        
    def _replace_vacancy_with_new_employee(self, manager, vacancy_index, new_employee_name):
        vacancy = manager.reports[vacancy_index]
        vacancy_reports = vacancy.reports
        new_employee = Employee(name=new_employee_name, role=vacancy.role, boss=manager)
        manager.reports[vacancy_index] = new_employee
        new_employee.reports = vacancy_reports
        self.all_names.add(new_employee_name)
        self.employee_lookup[new_employee_name] = new_employee
        print(f"Successfully placed {new_employee_name} under {manager.name}.")

    def _is_superior_to(self, manager, employee):
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
        # Removes an employee from the organization.
        # Remove employee name from tracking structures
        self.all_names.remove(employee.name)
        del self.employee_lookup[employee.name]

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
        print(f"Successfully placed {employee.name} under {new_boss.name}.")

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

    def _find_opening(self, manager, role):
        # Determines which helper method to call based on role.
        match role:
            case "Worker":
                return self._find_worker_opening(manager)
            case "Supervisor":
                return self._find_super_opening(manager)
            case "Vice President":
                return self._find_vp_opening(manager)
        return None, None

    def _find_worker_opening(self, supervisor):
        # Checks for worker openings in the company
        # Checks for empty spots under current Supervisor
        result = self._has_spots(supervisor)
        if result is True:
            return -1, supervisor
        # Checks for Vacancy objects under current Supervisor
        elif result != False:
            return result, supervisor
        # Otherwise, move to other Supervisors if they exist
        for report in supervisor.boss.reports:
            if report is not supervisor:
                result = self._has_spots(report)
                if result is True:
                    return -1, report
                elif result != False:
                    return result, report
        # No Worker openings found under current VP branch, move to other VP branch if it exists
        for vp in supervisor.boss.boss.reports:
            if vp is not supervisor.boss:
                for report in vp.reports:
                    result = self._has_spots(report)
                    if result is True:
                        return -1, report
                    elif result != False:
                        return result, report
        # No Worker openings found
        return None, None

    def _find_super_opening(self, vp):
        # Checks for supervisor openings in the company
        # Checks for empty spots under current VP
        result = self._has_spots(vp)
        if result is True:
            return -1, vp
        # Checks for Vacancy objects under current VP
        elif result != False:
            return result, vp
        # Otherwise, move to other VP if it exists
        for report in vp.boss.reports:
            if report is not vp:
                result = self._has_spots(report)
                if result is True:
                    return -1, report
                elif result != False:
                    return result, report

        # No Supervisor openings found
        return None, None

    def _find_vp_opening(self, president):
        # Checks if other VP spot is available
        result = self._has_spots(president)
        if result is True:
            return -1, president
        # Has Vacancy object
        elif result != False:
            return result, president
        # No Vice President openings found
        return None, None


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

        result = self._has_spots(hiring_manager)
        # Checks if there is an open spot
        if result is False:
            print(f"Error: Hiring manager {hiring_manager_name} has reached maximum direct reports.")
            return

        # Replace empty spot with new employee
        elif result is True:
            self._add_employee(hiring_manager, new_employee_name)

        # Replace Vacancy object with new employee
        else:
            self._replace_vacancy_with_new_employee(hiring_manager, result, new_employee_name)
       

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
        if not self._is_superior_to(firing_manager, target_employee):
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
        if not self._is_superior_to(manager, target_employee):
            print(f"Error: {manager_name} is not in the hierarchy of {target_employee_name}.")
            return

        index, new_boss = self._find_opening(target_employee.boss, target_employee.role)

        # If no opening found, remove employee
        if index is None:
            print(f"No comparable openings found")
            self._remove_employee(target_employee)
            print("Done")
            return

        # If opening found, transfer employee
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
        if not self._is_superior_to(initiator, employee):
            print(f"Error: {initiator_name} does not manage {employee_name}.")
            return

        # Checks if initiator manages destination manager, or if initiator is destination manager
        destination_manager = self._find_employee(destination_manager_name)
        if not self._is_superior_to(initiator, destination_manager) and initiator != destination_manager:
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
            # Need to decide on file structure first
            pass

        print(f"Successfully loaded organization from {filepath}.")
        return


    def display_organization(self):
        # Displays the current organization hierarchy (Requirement 11).
        if self.president is None:
            print("Organization is empty.")

        print(f"President: {self.president.name}")
        self._display_loop(self.president, 1)
        return