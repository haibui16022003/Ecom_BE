from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class WishlistBase(BaseModel):
    pass

class WishlistCreate(WishlistBase):
    user_id: UUID
    product_id: UUID
    
class WishlistResponse(WishlistBase):
    wish_id: UUID
    user_id: UUID
    product_id: UUID
    createdat: datetime
    # updatedat: datetime
    
    class config:
        orm_mode = True