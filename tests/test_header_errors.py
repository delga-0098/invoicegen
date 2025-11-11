from datetime import date
from typing import Any

import pytest

from invoicegen.models_header import (
    Address,
    BusinessInfo,
    ClientInfo,
    ContactInfo,
    InvoiceHeader,
    InvoiceMeta,
)


@pytest.fixture()
def base_address() -> dict:
    return {
        "line1": "1234 Main St.",
        "line2": "5678 Main St.",
        "city": "City",
        "state": "California",
        "postal_code": "12345",
    }


@pytest.fixture()
def base_contact_info() -> dict:
    return {"phone": "1234567890", "email": "johndoe123@gmail.com", "website": "example.com"}


@pytest.fixture()
def base_business() -> dict:
    return {
        "name": "Business Name",
        "logo": "logo.jpg",
        "license_number": "14L782P",
        "tax_id": "23-2098492",
    }


@pytest.fixture()
def base_client() -> dict:
    return {"name": "John Doe", "project_name": "Project 1"}


@pytest.fixture()
def base_meta() -> dict:
    return {"number": "INV-0001", "terms": "Net 30"}


def find_error(errors: list) -> Any:
    # Checks all the errors in the ErrorDetails List
    for err in errors:
        loc = err.get("loc", ())
        if loc:
            return err
    return None


def test_no_errors(
    base_address: dict,
    base_contact_info: dict,
    base_business: dict,
    base_client: dict,
    base_meta: dict,
) -> None:

    a = Address(**base_address)
    c = ContactInfo(**base_address)
    b = BusinessInfo(**{**base_business, "address": a, "contact": c})
    cli = ClientInfo(**{**base_client, "address": a, "contact": c})
    m = InvoiceMeta(**base_meta)
    header = InvoiceHeader(business=b, client=cli, meta=m)

    assert header.meta.start_date == date.today()
