from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Boolean, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.category_id"))
    name = Column(String(255), nullable=False)
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    active = Column(Boolean)
    imgproduct = Column(String(255))
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    wishlist = relationship("WishList", back_populates="product")
    cart_details = relationship("CartDetail", back_populates="product")
    invoice_details = relationship("InvoiceDetail", back_populates="product")