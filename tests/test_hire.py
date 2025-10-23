import pytest
from organization_manager import OrganizationManager

# ---------- HIRE TESTS ----------

def test_hire_valid_employee(capsys):
    """Test that a manager can successfully hire a valid employee."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    captured = capsys.readouterr()
    assert "Successfully hired" in captured.out
    assert "VP1" in org.employee_lookup


def test_hire_requires_existing_manager(capsys):
    """Hiring should fail if the intended manager position is vacant."""
    org = OrganizationManager()
    org.initialize_president("President1")

    # President hires a VP, then a Supervisor under that VP
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")

    # Fire the VP to create a Vacancy in that slot
    org.fire_employee("President1", "VP1")

    # Attempt to hire under the now-vacant VP spot
    org.hire_employee("VP1", "Supervisor2")
    captured = capsys.readouterr()

    # Assert correct failure message
    assert "does not exist" in captured.out


def test_hire_duplicate_name(capsys):
    """Test that hiring an employee with a duplicate name fails."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP1")  # duplicate name
    captured = capsys.readouterr()
    assert "already exists" in captured.out


def test_hire_worker_cannot_hire(capsys):
    """Test that a worker cannot hire anyone."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")
    org.hire_employee("Worker1", "Intern1")  # invalid
    captured = capsys.readouterr()
    assert "cannot hire" in captured.out


def test_hire_above_max_capacity_president(capsys):
    """Test that a manager cannot hire if at max capacity."""
    org = OrganizationManager()
    org.initialize_president("President1")
    # President can oversee up to 2 VPs
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")
    org.hire_employee("President1", "VP3")  # should fail
    captured = capsys.readouterr()
    assert "has reached maximum direct reports" in captured.out


def test_hire_within_capacity_president(with_president, capsys):
    with_president.hire_employee("Nelson", "VP1")
    out = capsys.readouterr().out
    assert "Successfully hired VP1 under Nelson." in out
    assert "has reached maximum direct reports" not in out


def test_hire_above_max_capacity_vice_president(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    # Vice President can oversee up to 3 Supervisors
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "S1")
    org.hire_employee("VP1", "S2")
    org.hire_employee("VP1", "S3")
    org.hire_employee("VP1", "S4") # should fail
    captured = capsys.readouterr()
    assert "has reached maximum direct reports" in captured.out


def test_hire_within_capacity_vice_president(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    # Vice President can oversee up to 5 Supervisors
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "S1")
    org.hire_employee("VP1", "S2")
    captured = capsys.readouterr()
    assert "Successfully hired S2" in captured.out
    assert "has reached maximum direct reports" not in captured.out


def test_hire_above_max_capacity_supervisor(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    # Supervisor can oversee up to 5 Workers
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "S1")
    org.hire_employee("S1", "W1")
    org.hire_employee("S1", "W2")
    org.hire_employee("S1", "W3")
    org.hire_employee("S1", "W4")
    org.hire_employee("S1", "W5")
    org.hire_employee("S1", "W6")  # should fail
    captured = capsys.readouterr()
    assert "has reached maximum direct reports" in captured.out


def test_hire_within_capacity_supervisor(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    # Supervisor can oversee up to 5 Workers
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "S1")
    org.hire_employee("S1", "W1")
    org.hire_employee("S1", "W2")
    captured = capsys.readouterr()
    assert "Successfully hired W2" in captured.out
    assert "has reached maximum direct reports" not in captured.out


def test_hire_fills_vacancy_after_fire(capsys):
    """Test that a manager can fill a vacancy left by a fired employee."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.fire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")  # fills vacancy
    captured = capsys.readouterr()
    assert "Successfully placed" in captured.out or "Successfully hired" in captured.out


def test_hire_cannot_fill_with_no_vacancy(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("President1", "VP2")
    org.fire_employee("President1", "VP2")
    org.hire_employee("President1", "VP3")
    org.hire_employee("President1", "VP4") # tries to fill an already filled position
    out = capsys.readouterr().out
    assert "has reached maximum direct reports" in out
