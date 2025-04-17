from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ProductBase(BaseModel):
    # category_id: UUID
    name: str
    quantity: Optional[int] = None
    price: Optional[float] = None
    active: Optional[bool] = None
    imgproduct: Optional[str] = None
    
class ProductCreate(ProductBase):
    category_id: UUID

class ProductResponse(ProductBase):
    category_id: UUID
    product_id: UUID
    createdat: datetime # Thêm trường createAt
    updatedat: datetime  # Thêm trường updateAt
    
    class Config:
        orm_mode = True  # Để sử dụng với SQLAlchemy ORM
