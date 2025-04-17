from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from uuid import UUID


#CART DETAIL
class CartDetailBase(BaseModel):
    product_id: UUID
    quantity: int
    
    
class CartDetailCreate(CartDetailBase):
    cartdetail_id: Optional[UUID] = None

class CartDetailResponse(CartDetailBase):
    cartdetail_id: UUID
    subtotal: Decimal
    
    class Config:
        orm_mode = True


# CART

class CartCreate(BaseModel):
    user_id: UUID
    details: List[CartDetailCreate]
    
class CartResponse(BaseModel):
    cart_id: UUID
    user_id: UUID
    totalprice: Decimal
    details: List[CartDetailResponse]
    createdat: datetime
    updatedat: datetime

    class Config:
        orm_mode = True