import pytest

def test_president_above_vps_max(with_president, capsys):
    # President can only be over up to 2 vice presidents
    with_president.hire_employee("Nelson", "VP1")
    with_president.hire_employee("Nelson", "VP2")
    capsys.readouterr()

    with_president.hire_employee("Nelson", "VP3")
    out = capsys.readouterr().out
    assert "Error: Hiring manager Nelson has reached maximum direct reports." in out

def test_president_within_vps_num(with_president, capsys):
    with_president.hire_employee("Nelson", "VP1")
    out = capsys.readouterr().out
    assert "Successfully hired VP1 under Nelson."