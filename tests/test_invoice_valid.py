from decimal import Decimal
from typing import Any

import pytest

from invoicegen.models import (
    Address,
    BusinessInfo,
    ClientInfo,
    Invoice,
    InvoiceHeader,
    InvoiceMeta,
    JobLine,
    Payment,
)


@pytest.fixture()
def base_address() -> Address:
    return Address(line1="1234 Main St.", city="City", state="California", postal_code="12345")


@pytest.fixture()
def base_business(base_address: Address) -> BusinessInfo:
    return BusinessInfo(name="Business Name", address=base_address)


@pytest.fixture()
def base_client(base_address: Address) -> ClientInfo:
    return ClientInfo(name="John Doe", address=base_address)


@pytest.fixture()
def base_meta() -> InvoiceMeta:
    return InvoiceMeta(
        number="INV-0001",
    )


@pytest.fixture()
def base_header(
    base_business: BusinessInfo, base_client: ClientInfo, base_meta: InvoiceMeta
) -> InvoiceHeader:
    return InvoiceHeader(business=base_business, client=base_client, meta=base_meta)


@pytest.fixture()
def jobline_list() -> list:
    job1: dict[str, Any] = {
        "address": "Elderwood",
        "unit": "A",
        "dates": "10/02/2025",
        "description": "Fix leak.",
        "qty": 1,
        "rate": 80,
        "source_row": 2,
    }
    job2: dict[str, Any] = {
        "address": "Elizabeth",
        "unit": "B",
        "dates": "10/11/2025",
        "description": "Fix toilet.",
        "qty": 1,
        "rate": 150,
        "source_row": 3,
    }
    job3: dict[str, Any] = {
        "address": "Elderwood",
        "unit": "A",
        "dates": "10/29/2025",
        "description": "Replace faucet.",
        "qty": 1,
        "rate": 125,
        "source_row": 4,
    }
    return [
        JobLine.model_validate(job1),
        JobLine.model_validate(job2),
        JobLine.model_validate(job3),
    ]


@pytest.fixture()
def payment_list() -> list:
    payment1: dict[str, Any] = {"dates": "10/8/2025", "amount": 10, "note": "Only $10."}
    payment2: dict[str, Any] = {"dates": "10/14/2025", "amount": 15}
    return [Payment.model_validate(payment1), Payment.model_validate(payment2)]


@pytest.fixture()
def base_invoice(base_header: InvoiceHeader, jobline_list: list, payment_list: list) -> dict:
    return {
        "header": base_header,
        "lines": jobline_list,
        "tax_rate": Decimal("8.25"),
        "payments": payment_list,
    }


def test_valid_invoice(base_invoice: dict) -> None:
    i = Invoice(**base_invoice)

    assert i.subtotal == Decimal("355")
    assert i.tax_total == Decimal("29.29")
    assert i.total == Decimal("384.29")
    assert i.amount_paid == Decimal("25")
    assert i.balance_due == Decimal("359.29")
