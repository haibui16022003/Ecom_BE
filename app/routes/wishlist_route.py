from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.wishlist_schema import WishlistResponse, WishlistCreate
from app.models.wishlist_model import WishList
from app.models.user_model import Users
from app.models.product_model import Product
from app.database import get_db
import logging
from uuid import UUID

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.get("/", response_model=list[WishlistResponse])
def get_all_wishlist(db: Session = Depends(get_db)):
    wishlists = db.query(WishList).all()
    return wishlists

@router.get("/{user_id}", response_model=list[WishlistResponse])
def get_wishlist_by_user(user_id: UUID, db: Session = Depends(get_db)):
    wishlist = db.query(WishList).filter(WishList.user_id == user_id).all()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist

@router.post("/", response_model=WishlistResponse)
def create_wishlist(wishlist: WishlistCreate, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_id == wishlist.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.query(Product).filter(Product.product_id == wishlist.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing_wishlist = db.query(WishList).filter(
        WishList.user_id == wishlist.user_id,
        WishList.product_id == wishlist.product_id
    ).first()
    if existing_wishlist:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
    try:
        new_wishlist = WishList(**wishlist.dict())
        db.add(new_wishlist)
        db.commit()
        db.refresh(new_wishlist)
        return new_wishlist
    except Exception as e:
        logging.error(f"Error creating wishlist: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
@router.delete("/{wishlist_id}", response_model=WishlistResponse)
def delete_wishlist(wishlist_id: UUID, db: Session = Depends(get_db)):
    wishlist = db.query(WishList).filter(WishList.wishlist_id == wishlist_id).first()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    try:
        db.delete(wishlist)
        db.commit()
        return wishlist
    except Exception as e:
        logging.error(f"Error deleting wishlist: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")