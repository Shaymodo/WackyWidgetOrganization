import pytest
from organization_manager import OrganizationManager

# ---------- FIRE TESTS ----------

def test_fire_valid_employee(capsys):
    """Manager successfully fires a direct report, leaving a vacancy."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.fire_employee("President1", "VP1")
    captured = capsys.readouterr()
    assert "has been removed from the company" in captured.out
    assert "VP1" not in org.employee_lookup


def test_fire_outside_hierarchy(capsys):
    """Test that firing someone outside your hierarchy fails."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")
    org.hire_employee("VP1", "Supervisor1")
    # VP2 tries to fire Supervisor1 (not in their hierarchy)
    org.fire_employee("VP2", "Supervisor1")
    captured = capsys.readouterr()
    assert "is not in the hierarchy" in captured.out


def test_fire_nonexistent_employee(capsys):
    """Test that firing a name that doesn’t exist is handled gracefully."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.fire_employee("President1", "VP1")
    captured = capsys.readouterr()
    assert "does not exist" in captured.out


def test_fire_nonexistent_manager(capsys):
    """Test firing with a manager name that doesn’t exist."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.fire_employee("GhostManager", "VP1")
    captured = capsys.readouterr()
    assert "does not exist" in captured.out


def test_fire_president_not_allowed(capsys):
    """Ensure firing the President is blocked."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.fire_employee("President1", "President1")
    captured = capsys.readouterr()
    assert "Cannot fire the President" in captured.out


