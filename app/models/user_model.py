from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import func
from sqlalchemy.orm import relationship
from app.database import Base

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    role = Column(String(50), nullable=True)
    rolecode = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    displayname = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    phonenumber = Column(String(10), nullable=True)
    password = Column(String(255), nullable=False)
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships (optional, for ORM linking)
    cart = relationship("Cart", back_populates="user", uselist=False)
    invoices = relationship("Invoice", back_populates="user")
    wishlist = relationship("WishList", back_populates="user")