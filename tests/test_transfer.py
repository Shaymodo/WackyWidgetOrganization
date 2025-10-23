import pytest
from organization_manager import OrganizationManager

# ---------- TRANSFER TESTS ----------

def test_transfer_valid_same_level(capsys):
    """Valid transfer of an employee to another manager at the same level."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")

    # VP1 hires a Supervisor
    org.hire_employee("VP1", "Supervisor1")

    # VP2 should have room for a Supervisor
    org.transfer_employee("President1", "Supervisor1", "VP2")
    captured = capsys.readouterr()
    assert "Successfully placed" in captured.out

def test_transfer_invalid_diff_level(capsys):
    """Valid transfer of an employee to another manager at the same level."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")

    # VP1 hires a Supervisor
    org.hire_employee("VP1", "Supervisor1")

    capsys.readouterr()

    # VP2 should have room for a Supervisor
    org.transfer_employee("President1", "Supervisor1", "President1")
    captured = capsys.readouterr()
    assert "Successfully placed" not in captured.out


def test_transfer_requires_authorized_initiator(capsys):
    """Transfer should fail if initiated by someone not authorized (e.g., Supervisor)."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("VP1", "Supervisor2")

    # Supervisor1 tries to initiate transfer — invalid
    org.transfer_employee("Supervisor1", "Supervisor2", "VP1")
    captured = capsys.readouterr()
    assert "does not have permission" in captured.out


def test_transfer_requires_vacancy(capsys):
    """Transfer should fail if destination manager has no open spots."""
    org = OrganizationManager()
    org.initialize_president("President1")

    # President oversees 2 VPs max
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")

    # VP1 hires a Supervisor
    org.hire_employee("VP1", "Supervisor1")

    # VP2 fills all 3 Supervisor spots
    org.hire_employee("VP2", "Supervisor2")
    org.hire_employee("VP2", "Supervisor3")
    org.hire_employee("VP2", "Supervisor4")

    # Attempt transfer into full VP2
    org.transfer_employee("President1", "Supervisor1", "VP2")
    captured = capsys.readouterr()
    assert "has reached maximum direct reports" in captured.out


def test_transfer_nonexistent_names(capsys):
    """Ensure transfer fails gracefully when invalid names are used."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.transfer_employee("President1", "GhostEmployee", "GhostManager")
    captured = capsys.readouterr()
    assert "does not exist" in captured.out


def test_transfer_allowed_by_vice_president(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")

    # President oversees 2 VPs max
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")

    # VP1 hires a Supervisor
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("VP1", "Supervisor2")

    # VP2 fills all 3 Supervisor spots
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Supervisor1", "Worker2")

    capsys.readouterr()

    org.transfer_employee("VP1", "Worker1", "Supervisor2")
    captured = capsys.readouterr()
    assert "Successfully" in captured.out
    

def test_transfer_initiator_not_control_source_and_dest(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("VP1", "Supervisor2")
    capsys.readouterr()
    # VP2 tries to initiate transfer — invalid
    org.transfer_employee("VP2", "Supervisor2", "VP2")
    captured = capsys.readouterr()
    assert "does not manage" in captured.out