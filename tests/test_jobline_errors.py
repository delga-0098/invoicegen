import pytest
from invoicegen.models import Jobline
from pydantic import ValidationError
from decimal import Decimal
from typing import Any


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

@pytest.mark.parametrize("field", ["address", "unit", "description"], ids= ["address", "unit", "description"])
@pytest.mark.parametrize("raw", [int(13), float(12.23), Decimal(22.98)], ids= ["int", "float", "decimal"])
def test_not_str_when_expected(field: str, raw: Any, base_jobline: dict) -> None:
    with pytest.raises(ValidationError) as exc:
        j = Jobline(**{**base_jobline, field: raw})
        
    err = find_error(exc.value.errors(), field, f"{field.capitalize()} must be a string, got {type(raw).__name__}")
    assert err

