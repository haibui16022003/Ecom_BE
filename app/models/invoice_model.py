from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoice"

    invoice_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(DateTime, server_default=func.now())
    totalprice = Column(DECIMAL(10, 2))
    status = Column(String(50))
    createdat=Column(DateTime, server_default=func.now())
    updatedat=Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("Users", back_populates="invoices")
    details = relationship("InvoiceDetail", back_populates="invoice")
    
class InvoiceDetail(Base):
    __tablename__ = "invoicedetail"

    invoicedetail_id = Column(UUID, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoice.invoice_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)
    subtotal = Column(DECIMAL(10, 2))

    invoice = relationship("Invoice", back_populates="details")
    product = relationship("Product", back_populates="invoice_details")