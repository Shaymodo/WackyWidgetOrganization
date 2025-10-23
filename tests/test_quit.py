import pytest
from organization_manager import OrganizationManager

# ---------- QUIT TESTS ----------

def test_quit_valid_employee(capsys):
    """Employee quits successfully, leaving a vacancy."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.employee_quits("VP1")
    captured = capsys.readouterr()
    assert "has been removed from the company" in captured.out
    assert "VP1" not in org.employee_lookup


def test_quit_president_not_allowed(capsys):
    """Ensure the President cannot quit."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.employee_quits("President1")
    captured = capsys.readouterr()
    assert "President cannot quit" in captured.out


def test_quit_nonexistent_employee(capsys):
    """Test quitting with a name that doesn’t exist."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.employee_quits("VP1")
    captured = capsys.readouterr()
    assert "does not exist" in captured.out


def test_quit_after_quit_already(capsys):
    """Test quitting after quitting already."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.employee_quits("VP1")
    org.employee_quits("VP1")
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
