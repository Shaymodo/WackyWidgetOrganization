import pytest

def test_display_with_president_prints_header(with_president, capsys):
    with_president.display_organization()
    out = capsys.readouterr().out
    assert "President: Nelson" in out

def test_display_without_president_prints_empty_and_does_not_crash(org, capsys):
    # No president initialized

    # Run display (should not raise)
    org.display_organization()
    out = capsys.readouterr().out
    assert "Organization is empty." in out
    # Must NOT contain "President:" line because there's no president
    assert "President:" not in out

def test_display_with_multiple_levels(org, capsys):
    org.initialize_president("Nelson")
    org.hire_employee("Nelson", "VP1")
    org.hire_employee("Nelson", "VP2")
    org.hire_employee("VP1", "S1")
    org.hire_employee("VP1", "S2")
    capsys.readouterr()

    expected_lines = [
        "President: Nelson",
        "\tVice President: VP1",
        "\t\tSupervisor: S1",
        "\t\tSupervisor: S2",
        "\tVice President: VP2",
    ]

    org.display_organization()
    out = capsys.readouterr().out
    assert out.splitlines() == expected_lines