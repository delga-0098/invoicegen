import re
from datetime import date, datetime, timedelta
from typing import Any

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator

"""
Need to create stronger validation for multiple fields, just checking for precense now.
"""


class Address(BaseModel):
    line1: str
    line2: str | None = None
    city: str
    state: str
    postal_code: str
    country: str = "US"

    @field_validator("line1", "city", "state", "postal_code", "country", mode="before")
    def ensure_nonempty_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        value = value.strip()

        # Check if it is empty
        if len(value) < 1:
            raise ValueError(f"{str(info.field_name).capitalize()} is empty, expected a value")

        return str(value)

    @field_validator("line2", mode="before")
    def ensure_optional_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # If it is the optional line 2 and it is empty, return None
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        s = value.strip()
        return s if s else None


class ContactInfo(BaseModel):
    phone: str | None = None  # TODO: Stronger validation
    email: str | None = None  # TODO: Stronger validation
    website: str | None = None

    @field_validator("phone", "email", "website", mode="before")
    def ensure_optional_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # If it is the optional line 2 and it is empty, return None
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        s = value.strip()
        return s if s else None


class BusinessInfo(BaseModel):
    name: str
    address: Address
    logo: str | None = None
    contact: ContactInfo | None = None
    license_number: str | None = None
    tax_id: str | None = None

    @field_validator("name", mode="before")
    def ensure_nonempty_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        value = value.strip()

        # Check if it is empty
        if len(value) < 1:
            raise ValueError(f"{str(info.field_name).capitalize()} is empty, expected a value")

        return str(value)

    @field_validator("tax_id", "logo", "license_number", mode="before")
    def ensure_optional_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # If it is the optional line 2 and it is empty, return None
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        s = value.strip()
        return s if s else None


class ClientInfo(BaseModel):
    name: str
    address: Address
    contact: ContactInfo | None = None
    project_name: str | None = None

    @field_validator("name", mode="before")
    def ensure_nonempty_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        value = value.strip()

        # Check if it is empty
        if len(value) < 1:
            raise ValueError(f"{str(info.field_name).capitalize()} is empty, expected a value")

        return str(value)

    @field_validator("project_name", mode="before")
    def ensure_optional_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # If it is the optional line 2 and it is empty, return None
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        s = value.strip()
        return s if s else None


class InvoiceMeta(BaseModel):
    number: str
    start_date: date | None = None
    due_date: date | None = None
    terms: str | None = None  # TODO: Stronger validation

    @field_validator("number", mode="before")
    def ensure_nonempty_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        value = value.strip()

        # Check if it is empty
        if len(value) < 1:
            raise ValueError(f"{str(info.field_name).capitalize()} is empty, expected a value")

        return str(value)

    @field_validator("start_date", mode="before")
    def validate_start_date(cls: Any, value: Any) -> date:
        if value is None:
            None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"Start date must be a string in MM/DD/YYYY format, got {type(value).__name__}"
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

    @field_validator("due_date", mode="before")
    def validate_due_date(cls: Any, value: Any) -> Any:
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"Due date must be a string in MM/DD/YYYY format, got {type(value).__name__}"
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

    @field_validator("terms", mode="before")
    def ensure_optional_str(cls: Any, value: str, info: ValidationInfo) -> Any:
        # If it is the optional line 2 and it is empty, return None
        if value is None:
            return None

        # Make sure it is a string
        if not isinstance(value, str):
            raise ValueError(
                f"{str(info.field_name).capitalize()} must be a string, got {type(value).__name__}"
            )

        s = value.strip()
        return s if s else None

    @model_validator(mode="after")
    def compute_due_date(self: Any) -> Any:
        if self.start_date is None:
            self.start_date = date.today()
        
        if self.due_date is not None:
            if self.due_date < self.start_date:
                raise ValueError("Due date must be after start date.")
            return self

        # Set due date based on terms
        if self.terms is None:
            self.due_date = self.start_date
        elif self.terms == "Net 15":
            self.due_date = self.start_date + timedelta(days=15)
        elif self.terms == "Net 30":
            self.due_date = self.start_date + timedelta(days=30)
        elif self.terms == "Net 30":
            self.due_date = self.start_date + timedelta(days=60)
        elif self.terms == "Net 30":
            self.due_date = self.start_date + timedelta(days=90)
        return self


class InvoiceHeader(BaseModel):
    business: BusinessInfo
    client: ClientInfo
    meta: InvoiceMeta
