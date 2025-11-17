from decimal import Decimal

import pytest

from invoicegen.config import InvoiceConfig, load_config
from invoicegen.models import Address, BusinessInfo, ContactInfo


@pytest.fixture()
def business_address() -> dict:
    return {
        "line1": "1234 main St.",
        "line2": "Suite 200",
        "city": "Los Angeles",
        "state": "CA",
        "postal_code": "90001",
    }


@pytest.fixture()
def business_contact() -> dict:
    return {
        "email": "info@formaconstruction.com",
        "phone": "(123) 123-1234",
        "website": "https://formaconstruction.com",
    }


@pytest.fixture()
def base_config() -> dict:
    return {
        "tax_rate": 0.0725,
        "currency": "$",
        "invoice_pattern": "ym_seq",
        "invoice_prefix": "INV-",
        "sequence_start": "0001",
    }


@pytest.fixture()
def default_business(business_address: dict, business_contact: dict) -> BusinessInfo:
    return BusinessInfo(
        name="Forma Construction",
        address=Address(**business_address),
        contact=ContactInfo(**business_contact),
        logo="logo.jpg",
        license_number="CSLB #1234567",
        tax_id="XX-XXXXXXX",
    )


def test_config_model(base_config: dict, default_business: BusinessInfo) -> None:
    config = InvoiceConfig(**{**base_config, "business_info": default_business})

    assert config.business_info == default_business
    assert config.currency == "$"
    assert config.tax_rate == Decimal("0.0725")
    assert config.invoice_pattern == "ym_seq"
    assert config.invoice_prefix == "INV-"
    assert config.sequence_start == Decimal("0001")


def test_config_loading(base_config: dict, default_business: BusinessInfo) -> None:
    config = load_config()
    default_config = InvoiceConfig(**{**base_config, "business_info": default_business})

    assert config == default_config
