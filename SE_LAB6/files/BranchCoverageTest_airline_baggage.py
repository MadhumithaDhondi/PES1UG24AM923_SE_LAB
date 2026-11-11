"""Lab 6 - Branch coverage tests for airline_baggage.py.

Goal: every decision (if / elif / else, and each side of `and`)
evaluates both True and False at least once, including boundaries.
Run:
    coverage run --branch -m pytest BranchCoverageTest_airline_baggage.py
    coverage report -m
"""
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ---------- baggage_fee ----------

# if cabin not in FREE_ALLOWANCE  -> True / False
def test_unknown_cabin_raises():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


# if weight_kg < 0  -> True / False (0 is the boundary, valid)
def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_zero_weight_is_valid():
    assert baggage_fee("economy", 0, "domestic", False) == 0


# if is_member and cabin != "business"
def test_member_economy_gets_extra_allowance():
    # True and True -> allowance 25
    assert baggage_fee("economy", 25, "domestic", True) == 0


def test_member_premium_gets_extra_allowance():
    # premium 25 + 10 = 35
    assert baggage_fee("premium", 36, "domestic", True) == 20


def test_member_business_no_extra_allowance():
    # True and False -> allowance stays 40
    assert baggage_fee("business", 45, "domestic", True) == 100


def test_non_member_no_extra_allowance():
    # False -> allowance stays 15
    assert baggage_fee("economy", 16, "domestic", False) == 20


# if excess <= 0  -> True (incl. exact boundary) / False
def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_exactly_at_allowance():
    assert baggage_fee("economy", 15, "domestic", False) == 0


# if route == "domestic" -> True / False ; if excess > 20 -> True / False
def test_domestic_small_excess():
    assert baggage_fee("economy", 20, "domestic", False) == 5 * 20


def test_international_small_excess():
    assert baggage_fee("economy", 20, "international", False) == 5 * 45


def test_excess_exactly_20_not_doubled():
    # excess = 20 -> rate not doubled
    assert baggage_fee("economy", 35, "domestic", False) == 20 * 20


# nested: if route == "international" -> True / False
def test_domestic_large_excess_doubled_no_surcharge():
    # excess 25, rate 20 * 2 = 40
    assert baggage_fee("economy", 40, "domestic", False) == 25 * 40


def test_international_large_excess_doubled_with_surcharge():
    # excess 25, rate 45 * 2 + 10 = 100
    assert baggage_fee("economy", 40, "international", False) == 25 * 100


def test_other_route_large_excess_no_surcharge():
    # route neither domestic nor international -> rate 45, doubled 90, no +10
    assert baggage_fee("economy", 40, "regional", False) == 25 * 90


# ---------- carry_on_ok ----------

# if is_infant -> True (items <= 2 True / False)
def test_infant_two_items_ok():
    assert carry_on_ok(10, 2, True) is True


def test_infant_three_items_not_ok():
    assert carry_on_ok(3, 3, True) is False


# if weight_kg > 7 -> True / False (7 is the boundary)
def test_carry_on_overweight():
    assert carry_on_ok(8, 1, False) is False


def test_carry_on_exactly_7kg_ok():
    assert carry_on_ok(7, 1, False) is True


# items <= 1 -> True / False
def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True


def test_carry_on_too_many_items():
    assert carry_on_ok(5, 2, False) is False


# ---------- check_in_status ----------

# if has_baggage -> True / False ; if is_international -> True / False
# if minutes >= cutoff ; elif minutes >= cutoff - 15 ; else
def test_baggage_domestic_open_at_cutoff():
    assert check_in_status(60, True, False) == "open"


def test_baggage_domestic_late():
    assert check_in_status(50, True, False) == "late"


def test_baggage_international_open():
    assert check_in_status(120, True, True) == "open"


def test_baggage_international_late_boundary():
    # cutoff 120, late starts exactly at 105
    assert check_in_status(105, True, True) == "late"


def test_baggage_international_closed():
    assert check_in_status(104, True, True) == "closed"


def test_no_baggage_domestic_open():
    assert check_in_status(45, False, False) == "open"


def test_no_baggage_domestic_late():
    assert check_in_status(35, False, False) == "late"


def test_no_baggage_domestic_closed():
    assert check_in_status(10, False, False) == "closed"


def test_no_baggage_international_open():
    # cutoff 45 + 60 = 105
    assert check_in_status(105, False, True) == "open"
