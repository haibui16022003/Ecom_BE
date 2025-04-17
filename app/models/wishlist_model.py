from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from app.database import Base

class WishList(Base):
    __tablename__ = "wishlist"

    wish_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    createdat = Column(DateTime, server_default=func.now())
    # updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("Users", back_populates="wishlist")
    product = relationship("Product", back_populates="wishlist")