from collections import defaultdict
from datetime import date

from invoicegen.config import InvoiceConfig
from invoicegen.models import Invoice, InvoiceHeader, JobLine

"""
Core invoice building engine.

This module converts the validated invoice objects into an Invoice object by doing the following:
- grouping job lines by project/address,
- sorting the lines in each project by date,
- computing the totals,
- generating the invoice numbers based on a pattern
- building an InvoiceHeader object based on provided information
"""

"""
Purpose

Parameters
----------
name : type
    What it is.

Returns
-------
type
    What it is.
"""


def group_by_project(job_lines: list[JobLine]) -> dict[str, list[JobLine]]:
    projects = defaultdict(list)
    for line in job_lines:
        projects[line.address].append(line)

    return projects


def sort_by_date(projects: dict[str, list[JobLine]]) -> dict[str, list[JobLine]]:
    for _project, jobs in projects.items():
        jobs.sort(key=lambda obj: obj.dates, reverse=False)

    return projects


def change_header(
    header: InvoiceHeader,
    invoice_number: str,
) -> InvoiceHeader:
    header.meta.number = invoice_number
    return header


def create_invoice(
    jobs: list[JobLine],
    header: InvoiceHeader,
    invoice_number: str,
    config: InvoiceConfig,
) -> Invoice:
    inv_header = change_header(header, invoice_number)

    return Invoice(
        header=inv_header,
        lines=jobs,
        currency=config.currency,
        tax_rate=config.tax_rate,
    )


def build_invoices(
    job_lines: list[JobLine],
    header: InvoiceHeader,
    config: InvoiceConfig,
) -> list[Invoice]:
    # Separate projects and sort them by date
    projects = group_by_project(job_lines)
    sorted_projects = sort_by_date(projects)

    seq = config.sequence_start
    invoices = []
    for project, jobs in sorted_projects.items():
        header.client.project_name = project
        # Determine numbering for invoices
        if config.invoice_pattern == "ym_seq":
            # {PREFIX}{YYYY}{MM}-{SEQ}

            # Retrieve date of the most recent job at that project
            last_date: date = jobs[-1].dates

            # Create the corresponding numbering prefix
            invoice_number = f"{config.invoice_prefix}{last_date.strftime('%Y%m')}{seq}"

            invoices.append(
                create_invoice(
                    jobs,
                    header,
                    invoice_number,
                    config,
                )
            )

            seq += 1

    config.sequence_start = seq
    return invoices
