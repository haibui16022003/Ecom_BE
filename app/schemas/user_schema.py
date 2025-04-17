from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    role: Optional[str] = None
    rolecode: Optional[str] = None
    active: Optional[bool] 
    displayname: Optional[str] = None
    address: Optional[str] = None
    phonenumber: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: UUID
    createdat: datetime
    updatedat: datetime

    class Config:
        orm_mode = True