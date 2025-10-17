from organization_manager import OrganizationManager

def incorrect_argument_count(command):
    print(f"Incorrect number of arguments for command {command}");

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
                if len(parts) != 4:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: HIRE <HiringManagerName> <NewEmployeeName> <Role>")
                    continue                
                # org_manager.hire_employee(parts[1], parts[2], parts[3])
            
            elif command == "FIRE":
                if len(parts) != 3:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: FIRE <FiringManagerName> <TargetEmployeeName>")
                    continue
                # org_manager.fire_employee(parts[1], parts[2])
                
            elif command == "QUIT":
                if len(parts) != 2:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: QUIT <TargetEmployeeName>")
                    continue
                # org_manager.employee_quits(parts[1])

            elif command == "LAYOFF":
                if len(parts) != 3:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: LAYOFF <ManagerName> <TargetEmployeeName>")
                    continue
                # org_manager.layoff_employee(parts[1], parts[2])
                
            elif command == "TRANSFER":
                if len(parts) != 4:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: TRANSFER <InitiatorName> <EmployeeName> <NewManagerName>")
                    continue
                # org_manager.transfer_employee(parts[1], parts[2], parts[3])

            elif command == "PROMOTE":
                if len(parts) != 3:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: PROMOTE <ReceivingManagerName> <TargetEmployeeName>")
                    continue
                # org_manager.promote_employee(parts[1], parts[2])

            elif command == "LOAD":
                if len(parts) != 2:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: LOAD <filepath>")
                    continue
                # org_manager.promote_employee(parts[1])

            elif command == "DISPLAY":
                if len(parts) != 1:
                    incorrect_argument_count(command)
                    print(f"Syntax should be: DISPLAY")
                    continue
                # org_manager.display_organization()


            else:
                print(f"Error: Unknown command '{command}'.")


        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
if __name__ == "__main__":
    main()