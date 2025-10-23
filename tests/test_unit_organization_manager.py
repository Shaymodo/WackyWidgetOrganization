# test_unit_organization_manager.py
import pytest
from organization_manager import OrganizationManager

# ---------- PRESIDENT / INIT TESTS ----------

def test_initialize_president_sets_structures_and_prevents_second(capsys):
    org = OrganizationManager()
    ok = org.initialize_president("President1")
    out = capsys.readouterr().out
    assert ok is True
    assert "Success: Initialized President President1" in out
    assert org.president is not None
    assert org.president.name == "President1"
    assert "President1" in org.all_names
    assert org.employee_lookup["President1"].role == "President"

    # second president not allowed
    ok2 = org.initialize_president("Other")
    assert ok2 is False
    assert org.president.name == "President1"

# ---------- HIRE TESTS ----------

def test_hire_under_president_creates_vp_and_tracks_names(capsys):
    org = OrganizationManager()
    org.initialize_president("President1")
    capsys.readouterr()

    org.hire_employee("President1", "VP1")
    out = capsys.readouterr().out
    assert "Successfully hired VP1 under President1" in out
    assert "VP1" in org.all_names
    assert org.employee_lookup["VP1"].role == "Vice President"
    assert org.employee_lookup["VP1"].boss.name == "President1"


def test_worker_cannot_hire(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("V1", "S1")
    org.hire_employee("S1", "W1")
    capsys.readouterr()

    org.hire_employee("W1", "X")
    out = capsys.readouterr().out
    assert "A worker cannot hire employees" in out
    assert "X" not in org.all_names


def test_hire_fails_when_supervisor_full(capsys):
    """Supervisor capacity is 5; 6th hire should fail."""
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("V1", "S1")
    org.hire_employee("S1", "W1")
    org.hire_employee("S1", "W2")
    org.hire_employee("S1", "W3")
    org.hire_employee("S1", "W4")
    org.hire_employee("S1", "W5")
    capsys.readouterr()

    org.hire_employee("S1", "W6")
    out = capsys.readouterr().out
    assert "has reached maximum direct reports" in out
    assert "W6" not in org.all_names

# ---------- FIRE / QUIT TESTS ----------

def test_fire_within_hierarchy_removes_worker_and_updates_lookup(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("V1", "S1")
    org.hire_employee("S1", "W1")
    capsys.readouterr()

    org.fire_employee("S1", "W1")
    out = capsys.readouterr().out
    assert "W1 has been removed from the company." in out
    assert "W1" not in org.all_names
    assert "W1" not in org.employee_lookup


def test_fire_outside_hierarchy_is_denied(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("P", "V2")
    org.hire_employee("V1", "S1")
    capsys.readouterr()

    org.fire_employee("V2", "S1")
    out = capsys.readouterr().out
    assert "is not in the hierarchy of" in out
    # State unchanged
    assert "S1" in org.employee_lookup
    assert org.employee_lookup["S1"].boss.name == "V1"


def test_president_cannot_quit(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    capsys.readouterr()

    org.employee_quits("P")
    out = capsys.readouterr().out
    assert "President cannot quit" in out
    assert org.president is not None

# ---------- TRANSFER TESTS ----------

def test_transfer_by_vp_succeeds_same_level_within_span(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("V1", "S1")
    org.hire_employee("V1", "S2")
    org.hire_employee("S1", "W1")

    capsys.readouterr()

    org.transfer_employee("V1", "W1", "S2")
    out = capsys.readouterr().out
    # Success message from _move_employee
    assert "Successfully placed W1 under S2" in out
    w1 = org.employee_lookup["W1"]
    assert w1.boss.name == "S2"
    assert w1 in org.employee_lookup["S2"].reports
    assert w1 not in org.employee_lookup["S1"].reports


def test_transfer_by_supervisor_is_denied(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("V1", "S1")
    org.hire_employee("V1", "S2")
    org.hire_employee("S1", "W1")
    capsys.readouterr()

    org.transfer_employee("S1", "W1", "S2")
    out = capsys.readouterr().out
    assert "does not have permission to transfer employees" in out
    # State unchanged
    w1 = org.employee_lookup["W1"]
    assert w1.boss.name == "S1"

# ---------- PROMOTION TESTS ----------

def test_promotion_receiving_vp_two_promotes_worker_one_level(capsys):
    """VP2 promotes W1 (from V1) to Supervisor under V2 (one level up, cross-org)."""
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("P", "V2")
    org.hire_employee("V1", "S1")
    org.hire_employee("S1", "W1")
    capsys.readouterr()

    org.promote_employee("V2", "W1")
    out = capsys.readouterr().out
    # Current implementation prints one of two success messages; assert role/state instead
    w1 = org.employee_lookup["W1"]
    assert w1.role == "Supervisor"
    assert w1.boss.name == "V2"

def test_promotion_by_source_org_is_denied(capsys):
    """Source org VP (V1) tries to promote W1 from V2—should be denied because receiving must initiate."""
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("P", "V2")
    org.hire_employee("V1", "S1")
    org.hire_employee("S1", "W1")
    capsys.readouterr()

    org.promote_employee("V1", "W1")
    out = capsys.readouterr().out
    assert "cannot promote employees" in out or "Error:" in out
    # W1 remains worker under S1
    w1 = org.employee_lookup["W1"]
    assert w1.role == "Worker"
    assert w1.boss.name == "S1"


def test_president_cannot_promote_worker_two_levels(capsys):
    """President promoting worker should be rejected (only one level promotions allowed)."""
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("P", "V2")
    org.hire_employee("V1", "S1")
    org.hire_employee("S1", "W1")
    capsys.readouterr()

    org.promote_employee("P", "W1")
    out = capsys.readouterr().out
    assert "Promotions can only be one level" in out
    w1 = org.employee_lookup["W1"]
    assert w1.role == "Worker"

# ---------- DISPLAY TESTS ----------

def test_display_outputs_structure(capsys):
    org = OrganizationManager()
    org.initialize_president("P")
    org.hire_employee("P", "V1")
    org.hire_employee("V1", "S1")
    capsys.readouterr()

    org.display_organization()
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert lines[0] == "President: P"
    assert "\tVice President: V1" in lines[1]
    assert "\t\tSupervisor: S1" in lines[2]
