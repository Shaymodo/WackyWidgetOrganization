import pytest
from organization_manager import OrganizationManager

# ---------- DISPLAY TESTS ----------

def test_display_basic_structure(capsys):
    """Display should show the president and direct reports in correct hierarchy."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")

    org.display_organization()
    captured = capsys.readouterr()

    assert "President: President1" in captured.out
    assert "Vice President: VP1" in captured.out
    assert "Supervisor: Supervisor1" in captured.out


def test_display_shows_vacancies_when_reports_exist(capsys):
    """Vacancies should appear only when a manager still has subordinates."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")
    org.hire_employee("VP1", "Supervisor1")
    org.hire_employee("Supervisor1", "Worker1")

    # Fire the supervisor to leave a vacancy
    org.fire_employee("VP1", "Supervisor1")

    org.display_organization()
    captured = capsys.readouterr()

    assert "VACANCY: Supervisor" in captured.out


def test_display_hides_vacancies_with_no_reports(capsys):
    """Vacancies should not display if they have no subordinates."""
    org = OrganizationManager()
    org.initialize_president("President1")
    org.hire_employee("President1", "VP1")

    # Fire VP — should leave a vacancy, but with no reports
    org.fire_employee("President1", "VP1")

    org.display_organization()
    captured = capsys.readouterr()

    # Expect no visible vacancy since no reports exist under that slot
    assert "VACANCY" not in captured.out


def test_display_empty_organization(capsys):
    """Display should handle empty or uninitialized organization gracefully."""
    org = OrganizationManager()
    org.display_organization()
    captured = capsys.readouterr()

    assert "Organization is empty" in captured.out
