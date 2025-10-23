import pytest
from organization_manager import OrganizationManager

# ---------- LAYOFF TESTS ----------

def test_layoff_relocates_to_same_supervisor(capsys):
    """Employee should relocate to another vacancy under the same supervisor if available."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Supervisor1", "Worker2")
    org.hire_employee("Supervisor1", "Worker3")
    org.hire_employee("Supervisor1", "Worker4")
    org.hire_employee("Supervisor1", "Worker5")

    # Fire one supervisor to create a vacancy under VP1
    org.fire_employee("Supervisor1", "Worker1")

    # Lay off Supervisor2, should move into Supervisor1's vacant slot
    org.layoff_employee("Supervisor1", "Worker2")
    captured = capsys.readouterr()
    assert "Successfully placed" in captured.out


def test_layoff_no_openings_removes_employee(capsys):
    """Employee is removed entirely if no comparable openings exist."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Supervisor1", "Worker2")
    org.hire_employee("Supervisor1", "Worker3")
    org.hire_employee("Supervisor1", "Worker4")
    org.hire_employee("Supervisor1", "Worker5") # All worker spots filled, no other job openings available

    # Remove employee since there are no other job openings available
    org.layoff_employee("Supervisor1", "Worker1")
    captured = capsys.readouterr()
    assert "No comparable openings found" in captured.out
    assert "Worker1" not in org.employee_lookup


def test_layoff_outside_hierarchy_fails(capsys):
    """Layoff should fail if the manager isn't in the employee's hierarchy."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")
    org.hire_employee("VP1", "Supervisor1")

    # VP2 tries to lay off Supervisor1 — invalid
    org.layoff_employee("VP2", "Supervisor1")
    captured = capsys.readouterr()
    assert "is not in the hierarchy" in captured.out


def test_layoff_president_not_allowed(capsys):
    """Ensure President cannot be laid off."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.layoff_employee("President1", "President1")
    captured = capsys.readouterr()
    assert "Cannot lay off the President" in captured.out

def test_layoff__with_opening_succeed_first_same_hierarchy(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")

    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Supervisor1", "Worker2")
    org.hire_employee("Supervisor1", "Worker3")
    org.hire_employee("Supervisor1", "Worker4")
    org.hire_employee("Supervisor1", "Worker5")

    org.hire_employee("VP1", "Supervisor2")
    org.hire_employee("Supervisor2", "Worker6") # Supervisor2 has vacancy

    org.hire_employee("VP2", "Supervisor3")
    org.hire_employee("Supervisor3", "Worker7") # different VP branch; also has vacancy

    org.layoff_employee("Supervisor1", "Worker5") # should check first within same hierarchy

    assert "Worker5" in org.employee_lookup
    worker5 = org.employee_lookup["Worker5"]

    assert worker5.boss is not None
    assert worker5.boss.name == "Supervisor2"

    super1 = org.employee_lookup["Supervisor1"]
    super2 = org.employee_lookup["Supervisor2"]
    assert worker5 in super2.reports
    assert worker5 not in super1.reports


def test_layoff__with_opening_succeed_diff_hierarchy(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")

    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Supervisor1", "Worker2")
    org.hire_employee("Supervisor1", "Worker3")
    org.hire_employee("Supervisor1", "Worker4")
    org.hire_employee("Supervisor1", "Worker5")

    org.hire_employee("VP2", "Supervisor2")
    org.hire_employee("Supervisor2", "Worker7") # different VP branch; has vacancy

    org.layoff_employee("Supervisor1", "Worker5")

    assert "Worker5" in org.employee_lookup
    worker5 = org.employee_lookup["Worker5"]

    assert worker5.boss is not None
    assert worker5.boss.name == "Supervisor2"

    super1 = org.employee_lookup["Supervisor1"]
    super2 = org.employee_lookup["Supervisor2"]
    assert worker5 in super2.reports
    assert worker5 not in super1.reports


