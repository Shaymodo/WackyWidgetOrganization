import pytest
from organization_manager import OrganizationManager

# ---------- PROMOTE TESTS ----------

def test_promote_valid_one_level(capsys):
    """Valid one-level promotion (Worker -> Supervisor or Supervisor -> VP)."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")

    # Promote Worker1 into the Supervisor vacancy
    org.promote_employee("VP1", "Worker1")
    captured = capsys.readouterr()
    assert "Successfully promoted" in captured.out


def test_promote_too_many_levels_fails(capsys):
    """Promotion should fail if skipping more than one level."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")

    # President tries to promote a Worker directly (2 levels)
    org.promote_employee("President1", "Worker1")
    captured = capsys.readouterr()
    assert "Promotions can only be one level" in captured.out


def test_promote_to_president_not_allowed(capsys):
    """Ensure promotion to President is blocked."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")

    # Attempt to promote VP to President (invalid)
    org.promote_employee("President1", "VP1")
    captured = capsys.readouterr()
    assert "cannot be promoted further" in captured.out


def test_promote_requires_vacancy(capsys): 
    """Promotion should fail if receiving manager has no open positions."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")

    # Max out supervisor spots
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("VP1", "Supervisor2")
    org.hire_employee("VP1", "Supervisor3")

    # Add workers to Supervisor1's Worker spots
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Supervisor1", "Worker2")

    # Attempt promotion to Supervisor position
    org.promote_employee("VP1", "Worker1")
    captured = capsys.readouterr()
    assert "has reached maximum direct reports" in captured.out


def test_promote_invalid_manager(capsys):
    """Promotion should fail if receiving manager does not exist."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.promote_employee("GhostManager", "VP1")
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
