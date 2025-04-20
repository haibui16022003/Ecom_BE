from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.models.user_model import Users
from app.database import get_db
import logging
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def get_All_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # JSON Error check
    # Role and rolecode validation
    if (user.rolecode != "ad" and user.rolecode != "us"):
        raise HTTPException(status_code=400, detail="Role code must be 'ad' or 'us'")
    if(user.rolecode == "ad" and user.role != "admin"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' with role code 'ad'")
    if (user.rolecode == "us" and user.role != "user"):
        raise HTTPException(status_code=400, detail="Role must be 'user' with role code 'us'")
    # phone number validation
    if len(user.phone) != 10 or not user.phone.isdigit():
        raise HTTPException(status_code=400, detail="Phone number must be 10 digits")
    if user.phone[0] != "0":
        raise HTTPException(status_code=400, detail="Phone number must start with 0")
    if user.phone[1] != "9" and user.phone[1] != "8" and user.phone[1] != "7" and user.phone[1] != "6" and user.phone[1] != "5" and user.phone[1] != "4" and user.phone[1] != "3" and user.phone[1] != "2":
        raise HTTPException(status_code=400, detail="Phone number must start with 09, 08, 07, 06, 05, 04, 03, 02")
    # password validation
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Check if user already exists
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="This username already exists")
    db_user = db.query(Users).filter(Users.email == user.email).first()
    # if db_user:
    #     raise HTTPException(status_code=400, detail="This email already exists")
    db_user = db.query(Users).filter(Users.phone == user.phone).first()
    if db_user:
        raise HTTPException(status_code=400, detail="This phone number already exists")
    try:
        new_user = Users(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.userid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.userid == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Chỉ cập nhật các trường được gửi trong JSON, bỏ qua createat và userid
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key not in ["createdat", "userid"]:  # Loại bỏ các trường không cần cập nhật
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.userid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}