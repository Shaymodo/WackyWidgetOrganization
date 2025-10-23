import pytest
from organization_manager import OrganizationManager
""" This is to test the requirement that: Must be one and only one president. """

def test_add_first_president_is_allowed():
    org = OrganizationManager()
    assert org.initialize_president("Dani") is True
    assert org.initialize_president is not None
    assert org.president.name == "Dani"

    assert "Dani" in org.all_names
    assert org.employee_lookup["Dani"].role == "President"

def test_cannot_add_second_president():
    with_president = OrganizationManager
    with_president.initialize_president("Nelson")
    assert with_president.president.name == "Nelson"
    assert with_president.initialize_president("Other") is False
    assert with_president.president.name == "Nelson"

def test_president_cannot_be_fired(capsys):
    with_president = OrganizationManager
    with_president.initialize_president("Nelson")
    with_president.fire_employee("Nelson", "Nelson")
    out = capsys.readouterr().out
    assert "Cannot fire the President" in out

    assert with_president.president is not None
    assert with_president.president.name == "Nelson"

def test_president_cannot_quit(capsys):
    with_president = OrganizationManager
    with_president.initialize_president("Nelson")
    with_president.employee_quits("Nelson")
    out = capsys.readouterr().out
    assert "President cannot quit" in out
    assert with_president.president is not None