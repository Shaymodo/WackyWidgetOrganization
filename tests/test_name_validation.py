import pytest
from organization_manager import OrganizationManager

def test_initialize_president_rejects_name_with_space():
    org = OrganizationManager()
    result = org.initialize_president("Ana Maria")
    # Desired behavior once validation added:
    assert result is False
    assert org.president is None

def test_hire_rejects_name_with_space():
    with_president = OrganizationManager
    with_president.initialize_president("Nelson")
    # set up a VP so we can hire properly
    with_president.hire_employee("Nelson", "V1")  # creates a VP under president
    # Attempt to hire an employee with a space under that VP
    with_president.hire_employee("V1", "Ana Maria")
    assert "Ana Maria" not in with_president.all_names
