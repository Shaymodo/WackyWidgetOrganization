# test_unit_employee.py
import pytest
from employee import Employee, Vacancy, ROLE_CAPACITY

# ---------- EMPLOYEE TESTS ----------

def test_employee_init_sets_fields():
    boss = Employee("VP1", "Vice President", None)
    e = Employee("Alice", "Supervisor", boss)
    assert e.name == "Alice"
    assert e.role == "Supervisor"
    assert e.boss is boss
    assert e.reports == []
    assert e.max_reports == ROLE_CAPACITY["Supervisor"] == 5

def test_employee_promote_worker_to_supervisor_updates_role_and_capacity():
    sup = Employee("S1", "Supervisor", None)
    w = Employee("W1", "Worker", sup)
    before = w.max_reports
    w.promote()
    assert w.role == "Supervisor"
    assert w.max_reports == ROLE_CAPACITY["Supervisor"]
    assert w.max_reports != before

def test_employee_promote_supervisor_to_vp_updates_role_and_capacity():
    vp = Employee("V1", "Vice President", None)
    s = Employee("S1", "Supervisor", vp)
    s.promote()
    assert s.role == "Vice President"
    assert s.max_reports == ROLE_CAPACITY["Vice President"] == 3

def test_employee_promote_vp_is_idempotent_for_role():
    """Promoting a VP should keep role 'Vice President' with same capacity (per current implementation)."""
    p = Employee("P", "President", None)
    v = Employee("V1", "Vice President", p)
    before_role = v.role
    before_cap = v.max_reports
    v.promote()  # no branch to promote VP in current code
    assert v.role == before_role == "Vice President"
    assert v.max_reports == before_cap == ROLE_CAPACITY["Vice President"]

# ---------- VACANCY / ORGANIZATIONSPOT TESTS ----------

def test_vacancy_init_and_capacity():
    p = Employee("P", "President", None)
    vac = Vacancy("Supervisor", p)
    assert vac.role == "Supervisor"
    assert vac.boss is p
    assert vac.reports == []
    assert vac.max_reports == ROLE_CAPACITY["Supervisor"]

def test_is_vacant_true_for_vacancy_false_for_employee():
    p = Employee("P", "President", None)
    v = Vacancy("Vice President", p)
    assert v.is_vacant() is True
    assert p.is_vacant() is False
