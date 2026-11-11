"""Lab 6 - Code (line) coverage tests for airline_baggage.py.

Goal: execute every statement in airline_baggage.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_airline_baggage.py
    coverage report -m
"""
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ---------- baggage_fee ----------

def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_unknown_cabin_raises():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_member_gets_extra_allowance():
    # economy 15 + member 10 = 25 kg free
    assert baggage_fee("economy", 20, "domestic", True) == 0


def test_domestic_small_excess():
    # 20 - 15 = 5 kg excess * 20
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_large_excess():
    # 40 - 15 = 25 kg excess; rate 45 doubled = 90, +10 international = 100
    assert baggage_fee("economy", 40, "international", False) == 2500


# ---------- carry_on_ok ----------

def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True


def test_carry_on_infant():
    assert carry_on_ok(10, 2, True) is True


def test_carry_on_overweight():
    assert carry_on_ok(8, 1, False) is False


# ---------- check_in_status ----------

def test_check_in_open_international_with_baggage():
    # cutoff = 60 + 60 = 120
    assert check_in_status(130, True, True) == "open"


def test_check_in_late_domestic_no_baggage():
    # cutoff = 45, late window 30-44
    assert check_in_status(35, False, False) == "late"


def test_check_in_closed():
    assert check_in_status(10, False, False) == "closed"
