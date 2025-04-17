from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime
from uuid import UUID

class InvoiceDetailResponse(BaseModel):
    invoicedetail_id: UUID
    product_id: UUID
    quantity: int
    subtotal: Decimal

    class Config:
        orm_mode = True

class InvoiceResponse(BaseModel):
    invoice_id: UUID
    user_id: UUID
    totalprice: Decimal
    status: str
    date: datetime
    createdat: datetime
    updatedat: datetime
    details: List[InvoiceDetailResponse]

    class Config:
        orm_mode = True
