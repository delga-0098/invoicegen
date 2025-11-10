import pytest
from invoicegen.models import Jobline
from pydantic import ValidationError
from decimal import Decimal
from typing import Any
from datetime import date


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

# Define a helper to help find the errors in the field
"""
ErrorDetails are formatted in
[
  {
    'type': 'value_error',
    'loc': ('dates',),
    'msg': "Invalid calendar date '10/32/2025' (MM/DD/YYYY)",
  },
  ...
]
"""
def find_error(errors: list, field: str, err_msg: str) -> Any:
    # Checks all the errors in the ErrorDetails List
    for err in errors:
        loc = err.get("loc", ())
        if loc and loc[0] == field and err_msg in err["msg"]:
            print(f"{err}")
            return err
    return None

@pytest.mark.parametrize("field", ["address", "unit", "description", "dates", "paid"], ids= ["address", "unit", "description", "dates", "paid"])
@pytest.mark.parametrize("raw", [int(13), float(12.23), Decimal(22.98)], ids= ["int", "float", "decimal"])
def test_not_str_when_expected(field: str, raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})
        
    err = find_error(exc.value.errors(), field, f"{field.capitalize()} must be a string")
    assert err

@pytest.mark.parametrize("field", ["address", "unit", "description"], ids= ["address", "unit", "description"])
@pytest.mark.parametrize("raw", ["", "          \t\n"], ids= ["empty", "whitespace"])
def  test_empty_str(field: str, raw: str, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, f"{field.capitalize()} is empty, expected a value")
    assert err

@pytest.mark.parametrize("raw", ['a' * 2001], ids= ["2001-chars"])
def test_description_max_chars(raw: str, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, "description": raw})

    err = find_error(exc.value.errors(), "description", "Description is too long (max 2000 chars)")
    assert err

@pytest.mark.parametrize("raw", ["2025-12-36", "naskd", "1234/123/9083"], ids= ["ISO", "invalid-date-format1", "invalid-date-format2"])
def test_invalid_date_format(raw: str, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, "dates": raw})

    err = find_error(exc.value.errors(), "dates", "Invalid date format")
    assert err

@pytest.mark.parametrize("raw", ["12/56/2004", "18/02/2018"], ids= ["invalid-day", "invalid-month",])
def test_invalid_calendar_date(raw: str, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, "dates": raw})

    err = find_error(exc.value.errors(), "dates", " Invalid calendar date")
    assert err

@pytest.mark.parametrize("field", ["qty", "rate"], ids= ["qty", "rate"])
@pytest.mark.parametrize("raw", [float(12), 123.534], ids= ["casted-float", "reg-float"])
def test_floated_value_error(field: str, raw: float, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, "must not be a float")

@pytest.mark.parametrize("field", ["qty", "rate"], ids= ["qty", "rate"])
@pytest.mark.parametrize("raw", [date(2025, 12, 12)], ids= ["date"])
def test_invalid_decimals_type(field: str, raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, "must be a string, int, or decimal")

@pytest.mark.parametrize("field", ["qty", "rate"], ids= ["qty", "rate"])
@pytest.mark.parametrize("raw", ["$$$", ",,,", ""], ids= ["dollar-sign", "commas", "empty"])
def test_decimals_empty_symbols(field: str, raw: str, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, "is empty after removing symbols; provide a number")

@pytest.mark.parametrize("field", ["qty", "rate"], ids= ["qty", "rate"])
@pytest.mark.parametrize("raw", ["$$asdk$", ".123"], ids= ["letters", "no-digits"])
def test_decimals_bad_format(field: str, raw: str, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, "must be digits.decimals")

@pytest.mark.parametrize("field", ["qty", "rate"], ids= ["qty", "rate"])
@pytest.mark.parametrize("raw", [Decimal("Infinity")], ids= ["Infinity"])
def test_decimals_not_finite(field: str, raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, "must be a finite number")

@pytest.mark.parametrize("field", ["qty", "rate"], ids= ["qty", "rate"])
@pytest.mark.parametrize("raw", [-1, Decimal("-200")], ids= ["negative-int", "negative-decimal",])
def test_decimals_negative(field: str, raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})

    err = find_error(exc.value.errors(), field, "must be at least 0")

@pytest.mark.parametrize("raw", [Decimal("8930"), 13, "fine"], ids= ["paid-decimal", "paid-int","paid-invalid-str"])
def test_paid_invalid_type(raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, "paid": raw})

    err = find_error(exc.value.errors(), "paid", "Paid must be a string or boolean")

@pytest.mark.parametrize("raw", [Decimal("12"), True], ids= ["source_row-decimal", "source_row-bool"])
def test_source_row_invalid_type(raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, "source_row": raw})

    err = find_error(exc.value.errors(), "source_row", "Source row must be an ints")

@pytest.mark.parametrize("raw", [1, -3], ids= ["source_row-one", "source_row-negative"])
def test_source_row_low(raw: int, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, "source_row": raw})

    err = find_error(exc.value.errors(), "source_row", "Source row must be greater than 2")