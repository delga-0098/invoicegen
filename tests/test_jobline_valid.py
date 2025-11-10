from datetime import date
from decimal import Decimal
from typing import Any

import pytest

from invoicegen.models import Jobline


# Create base jobline which will be modified in each case
@pytest.fixture
def base_jobline() -> dict:
    return {
        "address": "Elderwood",
        "unit": "A",
        "dates": "10/30/2025",
        "description": "Repaired leaking sink.",
        "qty": "1.5",
        "rate": "80",
        "source_row": 2,
    }


# Tests the base jobline for validity
def test_jobline_valid_path(base_jobline: dict) -> None:
    j = Jobline(**base_jobline)

    assert j.address == "Elderwood"
    assert j.unit == "A"
    assert j.description == "Repaired leaking sink."
    assert j.dates == date(2025, 10, 30)
    assert j.qty == Decimal("1.5")
    assert j.rate == Decimal("80")
    assert j.line_total == Decimal("120")


# Test whitespace trim
@pytest.mark.parametrize(
    "field", ["address", "unit", "description"], ids=["address", "unit", "description"]
)
@pytest.mark.parametrize(
    "raw, expected", [("    X    ", "X"), ("\tY\n", "Y")], ids=["spaces", "tabs"]
)
def test_whitespace_trim(field: str, raw: str, expected: str, base_jobline: dict) -> None:
    j = Jobline(**{**base_jobline, field: raw})

    assert getattr(j, field) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [("  10/30/2025  ", date(2025, 10, 30)), ("\t11/02/2013", date(2013, 11, 2))],
    ids=["dates-spaces", "dates-tabs"],
)
def test_dates_trimmed_and_parsed(raw: str, expected: date, base_jobline: dict) -> None:
    j = Jobline(**{**base_jobline, "dates": raw})

    assert j.dates == expected


@pytest.mark.parametrize("field", ["qty", "rate"], ids=["qty", "rate"])
@pytest.mark.parametrize(
    "raw, expected",
    [("    12    ", Decimal("12")), ("\t1.5\n", Decimal("1.5"))],
    ids=["spaces", "tabs"],
)
def test_decimals_trimmed_and_parsed(
    field: str, raw: str, expected: Decimal, base_jobline: dict
) -> None:
    j = Jobline(**{**base_jobline, field: raw})

    assert getattr(j, field) == expected


# Test that all valid types are accepted
@pytest.mark.parametrize("field", ["qty", "rate"], ids=["qty", "rate"])
@pytest.mark.parametrize(
    "raw, expected",
    [
        ("12.3115131", Decimal("12.3115131")),
        (15, Decimal("15")),
        (Decimal("17.2"), Decimal("17.2")),
    ],
    ids=["string", "integer", "decimal"],
)
def test_decimal_type_acceptances(
    field: str, raw: Any, expected: Decimal, base_jobline: dict
) -> None:
    j = Jobline(**{**base_jobline, field: raw})

    assert getattr(j, field) == expected


@pytest.mark.parametrize(
    "raw, expected", [("true", True), (False, False)], ids=["paid-string", "paid-bool"]
)
def test_paid_type_acceptance(raw: Any, expected: bool, base_jobline: dict) -> None:
    j = Jobline(**{**base_jobline, "paid": raw})

    assert j.paid == expected


@pytest.mark.parametrize("raw, expected", [(2, 2), (7, 7)], ids=["src-row-int1", "src-row-int2"])
def test_source_row_type_acceptance(raw: int, expected: int, base_jobline: dict) -> None:
    j = Jobline(**{**base_jobline, "source_row": raw})

    assert j.source_row == expected


# Test capitalization
@pytest.mark.parametrize(
    "raw, expected",
    [("True", True), ("FALSE", False)],
    ids=["capitalized-string", "all-capital-bool"],
)
def test_paid_capitalization_acceptance(raw: str, expected: bool, base_jobline: dict) -> None:
    j = Jobline(**{**base_jobline, "paid": raw})

    assert j.paid == expected


# Test rounding for calculated values
@pytest.mark.parametrize(
    "qty, rate, expected",
    [
        ("1.25", "3.25", Decimal("4.06")),
        ("4", "21.2395", Decimal("84.96")),
        ("2", "84.33796", Decimal("168.68")),
    ],
    ids=["total-under-five", "total-over-five", "total-five"],
)
def test_line_total_rounding(qty: str, rate: str, expected: Decimal, base_jobline: dict) -> None:
    j = Jobline(**{**base_jobline, "qty": qty, "rate": rate})

    assert j.line_total == expected


# Test valid symbol parsing
@pytest.mark.parametrize("field", ["qty", "rate"], ids=["qty", "rate"])
@pytest.mark.parametrize(
    "raw, expected",
    [("$12.3115131", Decimal("12.3115131")), ("1,458,547", Decimal("1458547"))],
    ids=["$ign", "comma"],
)
def test_decimal_symbol_parsing(
    field: str, raw: str, expected: Decimal, base_jobline: dict
) -> None:
    j = Jobline(**{**base_jobline, field: raw})

    assert getattr(j, field) == expected
