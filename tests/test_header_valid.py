import pytest


@pytest.fixture()
def base_address() -> dict:
    return {
        "line1": "1234 Main St.",
        "line2": "5678 Main St.",
        "city": "City",
        "state": "California",
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
