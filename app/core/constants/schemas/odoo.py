from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime


class LineItem(BaseModel):
    description: str
    quantity: int
    price_unit: float


class InvoiceSchema(BaseModel):
    tax_identification_customer: str
    tax_identification_supplier: str
    partner_id: str
    invoice_date: datetime
    invoice_number: str
    amount_total: float
    amount_untaxed: float
    tax_amount: float
    lines: Optional[List[LineItem]]

    @field_validator(
        "tax_identification_customer",
        "tax_identification_supplier",
        "partner_id",
        "invoice_date",
        "invoice_number",
    )
    @classmethod
    def not_empty(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("Field must not be empty")
        if value is None:
            raise ValueError("Field must not be empty")
        return value

    @field_validator("amount_total", "amount_untaxed", "tax_amount")
    @classmethod
    def positive_amount(cls, value):
        if value is None:
            raise ValueError("Amount cannot be None")
        if not isinstance(value, (int, float)):
            raise ValueError("Amount must be a number")
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value
