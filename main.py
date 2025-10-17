from organization_manager import OrganizationManager

def display_command_info(command, syntax, methods):
    print(f"\n--- Command: {command} ---")
    print(f"Usage Syntax: {syntax}")
    print(f"Internal Call: {methods}")
    print("-------------------------")

def main():
    org_manager = OrganizationManager()
    
    # President Placeholder
    org_manager.initialize_president("Mr. Wacky")

    print("\nWelcome to the Wacky Widget Company System.")
    print("Available commands: HIRE, FIRE, QUIT, LAYOFF, TRANSFER, PROMOTE, LOAD, DISPLAY, EXIT.")

    while True:
        try:
            user_input = input("\nEnter command: ").strip().upper()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]

            # Exit condition
            if command == "EXIT":
                print("Exiting Wacky Widget HR System. Goodbye!")
                break


            # Displays command info for now
            if command == "HIRE":
                display_command_info(
                    command,
                    "HIRE <HiringManagerName> <NewEmployeeName> <Role>",
                    "org_manager.hire_employee(manager_name, new_name, role)"
                )
            
            elif command == "FIRE":
                display_command_info(
                    command,
                    "FIRE <FiringManagerName> <TargetEmployeeName>",
                    "org_manager.fire_employee(manager_name, target_name)"
                )
                
            elif command == "QUIT":
                display_command_info(
                    command,
                    "QUIT <TargetEmployeeName>",
                    "org_manager.employee_quits(target_name)"
                )

            elif command == "LAYOFF":
                display_command_info(
                    command,
                    "LAYOFF <ManagerName> <TargetEmployeeName>",
                    "org_manager.layoff_employee(manager_name, target_name)"
                )
                
            elif command == "TRANSFER":
                display_command_info(
                    command,
                    "TRANSFER <InitiatorName> <EmployeeName> <NewManagerName>",
                    "org_manager.transfer_employee(initiator_name, employee_name, destination_manager_name)"
                )

            elif command == "PROMOTE":
                display_command_info(
                    command,
                    "PROMOTE <ReceivingManagerName> <TargetEmployeeName>",
                    "org_manager.promote_employee(receiving_manager_name, target_name)"
                )

            elif command == "LOAD":
                display_command_info(
                    command,
                    "LOAD <filepath>",
                    "org_manager.load_organization_from_file(filepath)"
                )

            elif command == "DISPLAY":
                display_command_info(
                    command,
                    "DISPLAY",
                    "org_manager.display_organization()"
                )

            else:
                print(f"Error: Unknown command '{command}'.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
if __name__ == "__main__":
    main()