from invoicegen.core import build_invoices
import pytest
from invoicegen.models import JobLine, InvoiceHeader, ClientInfo, Address, InvoiceMeta, Invoice
from invoicegen.config import load_config, InvoiceConfig
from decimal import Decimal

@pytest.fixture()
def base_job_lines() -> list[JobLine]:
    return [
        JobLine(
            dates="11/1/2024",
            address="Elderwood",
            unit="A",
            description="Repair leaking toilet.",
            rate=100,
            qty=1,
            source_row=2
        ),
        JobLine(
            dates="11/10/2024",
            address="Elderwood",
            unit="Single",
            description="Change doorknob.",
            rate=100,
            qty=1,
            source_row=3
        ),
        JobLine(
            dates="11/8/2024",
            address="Elderwood",
            unit="Single",
            description="Paint exerything.",
            rate=1000,
            qty=1,
            source_row=4
        ),
        JobLine(
            dates="11/10/2024",
            address="Elderwood",
            unit="Single",
            description="Clean bathroom.",
            rate=150,
            qty=1,
            source_row=5
        ),
        JobLine(
            dates="2/19/2025",
            address="Elizabeth",
            unit="G",
            description="Unclog sink.",
            rate=80,
            qty=1,
            source_row=6
        ),
        JobLine(
            dates="12/29/2021",
            address="Hill",
            unit="Front",
            description="Repair leak.",
            rate=100,
            qty=1,
            source_row=7
        ),
        JobLine(
            dates="11/16/2024",
            address="Hill",
            unit="A",
            description="Repair leaking toilet.",
            rate=80,
            qty=1,
            source_row=8
        ),
        JobLine(
            dates="11/15/2024",
            address="Hill",
            unit="A",
            description="Repair toilet floater.",
            rate=75,
            qty=1,
            source_row=9
        ),
        JobLine(
            dates="11/1/2024",
            address="Elizabeth",
            unit="B",
            description="Repair leaking sink.",
            rate=80,
            qty=1,
            source_row=10
        ),
        JobLine(
            dates="11/1/2024",
            address="Elizabeth",
            unit="D",
            description="Repair hole in wall.",
            rate=80,
            qty=1,
            source_row=11
        )
    ]

@pytest.fixture() 
def base_config() -> InvoiceConfig:
    return load_config()

@pytest.fixture()
def base_header() -> InvoiceHeader:
    client = ClientInfo(
        name="John Doe",
        address=Address(
            line1="1234 Main St.",
            line2="5678 Main St.",
            city="City",
            state="California",
            postal_code="12345"
        )
    )
    return InvoiceHeader(business=load_config().business_info, meta=InvoiceMeta(number="Placeholder"), client=client)

@pytest.fixture()
def base_invoice_list(base_header: InvoiceHeader) -> list[Invoice]:
    header1 = base_header 
    header1.meta.number = "INV-202411-0001"
    header1.client.project_name = "Elderwood"
    job_list1 = [
        JobLine(
            dates="11/1/2024",
            address="Elderwood",
            unit="A",
            description="Repair leaking toilet.",
            rate=100,
            qty=1,
            source_row=2
        ),
        JobLine(
            dates="11/8/2024",
            address="Elderwood",
            unit="Single",
            description="Paint exerything.",
            rate=1000,
            qty=1,
            source_row=4
        ),
        JobLine(
            dates="11/10/2024",
            address="Elderwood",
            unit="Single",
            description="Change doorknob.",
            rate=100,
            qty=1,
            source_row=3
        ),
        JobLine(
            dates="11/10/2024",
            address="Elderwood",
            unit="Single",
            description="Clean bathroom.",
            rate=150,
            qty=1,
            source_row=5
        )
    ]
    invoice1 = Invoice(
        header= header1,
        lines= job_list1,
        currency= "$",
        tax_rate= Decimal("0.0725")
    )

    header2= base_header
    header2.meta.number = "INV-202502-0002"
    header2.client.project_name = "Elizabeth"
    job_list2 = [
        JobLine(
            dates="11/1/2024",
            address="Elizabeth",
            unit="B",
            description="Repair leaking sink.",
            rate=80,
            qty=1,
            source_row=10
        ),
        JobLine(
            dates="11/1/2024",
            address="Elizabeth",
            unit="D",
            description="Repair hole in wall.",
            rate=80,
            qty=1,
            source_row=11
        ),
        JobLine(
            dates="2/19/2025",
            address="Elizabeth",
            unit="G",
            description="Unclog sink.",
            rate=80,
            qty=1,
            source_row=6
        ),
    ]
    invoice2 = Invoice(
        header= header2,
        lines= job_list2,
        currency= "$",
        tax_rate= Decimal("0.0725")
    )

    header3= base_header
    header3.meta.number = "INV-202411-0003"
    header3.client.project_name = "Hill"
    job_list3 = [
        JobLine(
            dates="12/29/2021",
            address="Hill",
            unit="Front",
            description="Repair leak.",
            rate=100,
            qty=1,
            source_row=7
        ),
        JobLine(
            dates="11/15/2024",
            address="Hill",
            unit="A",
            description="Repair toilet floater.",
            rate=75,
            qty=1,
            source_row=9
        ),
        JobLine(
            dates="11/16/2024",
            address="Hill",
            unit="A",
            description="Repair leaking toilet.",
            rate=80,
            qty=1,
            source_row=8
        )
    ]
    invoice3 = Invoice(
        header= header3,
        lines= job_list3,
        currency= "$",
        tax_rate= Decimal("0.0725")
    )
    return [invoice1, invoice2, invoice3]



def test_invoice_generation(base_job_lines: list[JobLine], base_header: InvoiceHeader, base_config: InvoiceConfig, base_invoice_list: list[Invoice]) -> None:
    invoice_list = build_invoices(base_job_lines, base_header, base_config)

    print(base_invoice_list)
    print(invoice_list)
    assert invoice_list == base_invoice_list
