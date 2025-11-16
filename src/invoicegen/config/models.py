from decimal import Decimal
from typing import Literal
from pathlib import Path
import yaml

from pydantic import BaseModel, ConfigDict, Field

from invoicegen.models.header import BusinessInfo


class InvoiceConfig(BaseModel):
    # Company information
    business_info: BusinessInfo

    # Taxing information
    tax_rate: Decimal = Field(
        default=Decimal("0"), description="Sales tax as a decimal, e.g. 0.095, for 9.5%"
    )

    # Invoice numbering information
    invoice_pattern: Literal["ym_unit_seq", "ym_seq", "simple_seq"] = Field(
        default="ym_seq", description="ym_unit_seq -> pre-YYYY-MM-UNIT-SEQ, etc."
    )
    invoice_prefix: str = Field(default="", description="Fixed prefix for invoice numbers.")
    sequence_start: Decimal = Field(default=Decimal("1"), ge=0, description="Starting sequence number.")

    # Currency label information
    currency: str = Field(
        default="USD$",
        min_length=1,
        max_length=16,
        description="Currency label printed on invoice, e.g. USD, $, MXN.",
    )

    model_config = ConfigDict(extra="ignore")

def load_config(config_dir: str | Path | None = None) -> InvoiceConfig:
    if config_dir is None:
        base_dir = Path(__file__).parent
    else:
        base_dir = Path(config_dir)

    with (base_dir / "invoicegen.yaml").open("r", encoding="utf-8") as f:
        raw_cfg = yaml.safe_load(f) or {}

    with (base_dir / "business.yaml").open("r", encoding="utf-8") as f:
        raw_business = yaml.safe_load(f) or {}

    if "tax_rate" in raw_cfg:
        raw_cfg["tax_rate"] = Decimal(str(raw_cfg["tax_rate"]))

    business_info = BusinessInfo(**raw_business)
    raw_cfg["business_info"] = business_info

    return InvoiceConfig(**raw_cfg)