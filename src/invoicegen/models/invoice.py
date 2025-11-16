import re
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator

from .header import InvoiceHeader
from .jobline import JobLine

TWO = Decimal("0.01")


def q2(x: Decimal) -> Decimal:
    return x.quantize(TWO, rounding=ROUND_HALF_UP)


class Payment(BaseModel):
    dates: date
    amount: Decimal
    note: str | None = None

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

    @field_validator("amount", mode="before")
    def validate_decimals(cls: Any, value: Any) -> Decimal:
        # We do not want any floats for precision
        if isinstance(value, float):
            raise ValueError(
                "Payment amount must not be a float, please use string, decimal, or int"
            )

        # Make sure input is a string, integer, or decimal
        if not isinstance(value, (str, int, Decimal)):
            raise ValueError(
                f"Payment amount must be a string, int, or decimal, got {type(value).__name__}"
            )

        # If the instance is a string, then prepare it to be converted to Decimal
        if isinstance(value, str):
            # Remove empty space, commas, and dollar signs
            value = value.strip().replace("$", "").replace(",", "")

            # If after removing non number characters, the string is empty
            if not len(value):
                raise ValueError("Payment amount is empty after removing symbols; provide a number")

            # Make sure pattern is a decimal number
            if not re.fullmatch(r"^[0-9]+(\.[0-9]+)?$", value):
                raise ValueError("Payment amount must be digits.decimals (e.g. 1.5, 65)")

        # Since now should only have values that can be converted to Decimals, convert it
        dec = q2(Decimal(value))

        # We only allow decimals that are finite and at least 0
        if not dec.is_finite():
            raise ValueError("Payment amount must be a finite number")
        if dec < 0:
            raise ValueError(f"Payment amount must be at least 0: got {dec}")

        return dec

    @field_validator("note", mode="before")
    def ensure_optional_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        # If string is empty, allow it
        s = value.strip()
        return s if s else None


class Invoice(BaseModel):
    header: InvoiceHeader
    lines: list[JobLine]
    currency: str = "USD$"
    tax_rate: Decimal = Decimal("0")
    payments: list[Payment] | None = None

    # Computed values
    subtotal: Decimal | None = None
    tax_total: Decimal | None = None
    total: Decimal | None = None
    amount_paid: Decimal | None = None
    balance_due: Decimal | None = None

    @field_validator("lines", mode="before")
    def verify_line_items_exist(cls: Any, value: list, info: ValidationInfo) -> list:
        if not isinstance(value, list):
            raise ValueError(
                f"{str(info.field_name)} must be a list of JobLines, got {type(value).__name__}"
            )

        if not value:
            raise ValueError("Job Lines are empty, must include at least one line")

        return value

    @field_validator("tax_rate", mode="before")
    def verify_valid_tax_rate(cls: Any, value: Decimal) -> Any:
        if not isinstance(value, Decimal):
            raise ValueError("Tax rate should be a decimal number between 0 and 100")

        max_percent = Decimal("100")
        if not (0 <= value <= max_percent):
            raise ValueError("Tax rate should be between 0 and 100")

        return value / max_percent

    @field_validator("payments", mode="before")
    def verify_payments_exist(cls: Any, value: list, info: ValidationInfo) -> Any:
        if value is None:
            return None

        if not isinstance(value, list):
            raise ValueError(
                f"{str(info.field_name)} must be a list of payments, got {type(value).__name__}"
            )

        return value if value else None

    @model_validator(mode="after")
    def compute_values(self: Any) -> Any:
        sub = Decimal(0)
        paid = Decimal(0)
        for line in self.lines:
            sub += line.line_total

        if self.payments:
            for payment in self.payments:
                paid += payment.amount

        self.amount_paid = q2(paid)
        self.subtotal = q2(sub)
        self.tax_total = q2(self.subtotal * (self.tax_rate if self.tax_rate else 0))
        self.total = self.subtotal + self.tax_total
        self.balance_due = self.total - self.amount_paid

        return self
