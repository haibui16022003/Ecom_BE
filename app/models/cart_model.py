from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    totalprice = Column(DECIMAL(10, 2))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("Users", back_populates="cart", uselist=False)
    details = relationship("CartDetail", back_populates="cart", cascade="all, delete-orphan")

class CartDetail(Base):
    __tablename__ = "cartdetail"

    cartdetail_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("cart.cart_id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.product_id"))
    subtotal = Column(DECIMAL(10, 2))
    quantity = Column(Integer)

    cart = relationship("Cart", back_populates="details")
    product = relationship("Product", back_populates="cart_details")