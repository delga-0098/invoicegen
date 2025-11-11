from datetime import date

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
    return {
        "number": "INV-0001",
        "start_date": "12/01/2025",
        "due_date": "12/16/2025",
        "terms": "Net 30",
    }


def test_happy_path(
    base_address: dict,
    base_contact_info: dict,
    base_business: dict,
    base_client: dict,
    base_meta: dict,
) -> None:

    a = Address(**base_address)
    c = ContactInfo(**base_contact_info)
    b = BusinessInfo(**{**base_business, "address": a, "contact": c})
    cli = ClientInfo(**{**base_client, "address": a, "contact": c})
    m = InvoiceMeta(**base_meta)
    header = InvoiceHeader(business=b, client=cli, meta=m)

    assert a.line1 == "1234 Main St."
    assert a.line2 == "5678 Main St."
    assert a.city == "City"
    assert a.state == "California"
    assert a.country == "US"
    assert c.phone == "1234567890"
    assert c.email == "johndoe123@gmail.com"
    assert c.website == "example.com"
    assert b.name == "Business Name"
    assert b.logo == "logo.jpg"
    assert b.license_number == "14L782P"
    assert b.tax_id == "23-2098492"
    assert cli.name == "John Doe"
    assert cli.project_name == "Project 1"
    assert m.number == "INV-0001"
    assert m.start_date == date(2025, 12, 1)
    assert m.due_date == date(2025, 12, 16)
    assert m.terms == "Net 30"
    assert header.business == b
    assert header.meta == m
    assert header.client == cli


def test_defaults(
    base_address: dict,
    base_business: dict,
    base_client: dict,
    base_meta: dict,
) -> None:

    del base_address["line2"]
    del base_business["logo"], base_business["license_number"], base_business["tax_id"]
    del base_client["project_name"]
    del base_meta["start_date"], base_meta["due_date"], base_meta["terms"]

    a = Address(**base_address)
    c = ContactInfo()
    b = BusinessInfo(**{**base_business, "address": a})
    cli = ClientInfo(**{**base_client, "address": a})
    m = InvoiceMeta(**base_meta)
    header = InvoiceHeader(business=b, client=cli, meta=m)

    assert a.line2 is None
    assert a.country == "US"
    assert c.phone is None
    assert c.email is None
    assert c.website is None
    assert b.logo is None
    assert b.license_number is None
    assert b.tax_id is None
    assert cli.project_name is None
    # assert m.start_date == date.today()
    # assert m.due_date == date.today() + timedelta(days=0)
    assert m.terms is None
    assert header
