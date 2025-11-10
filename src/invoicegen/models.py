import re
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class Jobline(BaseModel):
    address: str
    unit: str
    dates: date
    description: str
    qty: Decimal
    rate: Decimal
    line_total: Decimal | None = None
    paid: bool = False
    source_row: int

    @field_validator("address", "unit", mode="before")
    def ensure_nonempty_str(cls: Any, value: Any, info: ValidationInfo) -> str:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(f"{info.field_name.capitalize()} must be a string, got {type(value).__name__}")

        value = value.strip()

        # Check if it is empty
        if len(value) < 1:
            raise ValueError(f"{info.field_name.capitalize()} is empty, expected a value")

        return str(value)

    @field_validator("description", mode="before")
    def ensure_valid_decription(cls: Any, value: Any) -> str:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(f"Description must be a string, got {type(value).__name__}")

        value = value.strip()

        # Check if it is empty
        if len(value) < 1:
            raise ValueError("Description is empty, expected a value")
        
        # Check if description is less than 2000 characters long
        max_chars = 2000
        if len(value) > max_chars:
            raise ValueError("Description is too long (max 2000 chars)")

        return str(value)

    @field_validator("dates", mode="before")
    def validate_date(cls: Any, value: Any) -> date:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"Dates must be a string in MM/DD/YYYY format, got {type(value).__name__}"
            )

        value = value.strip()

        # Check expected fromat
        if not re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", value):
            raise ValueError(f"Invalid date format '{value}' (expected MM/DD/YYYY)")

        # Parse to real date object
        try:
            parsed = datetime.strptime(value, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError(f"Invalid calendar date '{value}' (MM/DD/YYYY)") from None

        return parsed

    @field_validator("qty", "rate", mode="before")
    def validate_decimals(cls: Any, value: Any, info: ValidationInfo) -> Decimal:
        # We do not want any floats for precision
        if isinstance(value, float):
            raise ValueError(
                f"{info.field_name.capitalize()} must not be a float, please use string, decimal, or int"
            )

        # Make sure input is a string, integer, or decimal
        if not isinstance(value, (str, int, Decimal)):
            raise ValueError(
                f"{info.field_name.capitalize()} must be a string, int, or decimal, got {type(value).__name__}"
            )

        # If the instance is a string, then prepare it to be converted to Decimal
        if isinstance(value, str):
            # Remove empty space, commas, and dollar signs
            value = value.strip().replace("$", "").replace(",", "")

            # If after removing non number characters, the string is empty
            if not len(value):
                raise ValueError(
                    f"{info.field_name.capitalize()} is empty after removing symbols; provide a number"
                )

            # Make sure pattern is a decimal number
            if not re.fullmatch(r"^[0-9]+(\.[0-9]+)?$", value):
                raise ValueError(f"{info.field_name.capitalize()} must be digits.decimals (e.g. 1.5, 65)")

        # Since now should only have values that can be converted to Decimals, convert it
        dec = Decimal(value)

        # We only allow decimals that are finite and at least 0
        if not dec.is_finite():
            raise ValueError(f"{info.field_name.capitalize()} must be a finite number")
        if dec < 0:
            raise ValueError(f"{info.field_name.capitalize()} must be at least 0: got {dec}")

        return dec

    @field_validator("paid", mode="before")
    def validate_paid(cls: Any, value: Any) -> bool:
        if isinstance(value, bool):
            value = f"{value}"

        if isinstance(value, str):
            value = value.strip().lower()

        if value == "true":
            return True
        elif value == "false":
            return False

        raise ValueError("Paid must be a string or boolean True or False")

    @field_validator("source_row", mode="before")
    def validate_row(cls: Any, value: Any) -> int:
        if not isinstance(value, int):
            raise ValueError(
                f"Source row must be an int, got {type(value).__name__}, how did this happen?"
            )
        if value < int("2"):
            raise ValueError("Source row must be greater than 2, you messed up the code")
        return value

    @model_validator(mode="after")
    def compute_line_total(self: Any) -> Any:
        # Calculate line total and round up to the nearest hundredth
        raw = self.qty * self.rate
        self.line_total = raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return self
