from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart_model import Cart, CartDetail
from app.models.product_model import Product
from app.schemas.cart_schema import CartCreate, CartResponse
from uuid import UUID

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/{user_id}", response_model=CartResponse)
def get_cart_by_user_id(user_id: UUID, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/", response_model=CartResponse)
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
     # Kiểm tra nếu user đã có cart
    existing_cart = db.query(Cart).filter(Cart.user_id == cart.user_id).first()
    if existing_cart:
        raise HTTPException(status_code=400, detail="User already has a cart")
    
    total_price = 0
    db_cart = Cart(user_id=cart.user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    for detail in cart.details:
        product = db.query(Product).filter(Product.product_id == detail.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {detail.product_id} not found")

        subtotal = product.price * detail.quantity
        total_price += subtotal

        db_detail = CartDetail(
            cart_id=db_cart.cart_id,
            product_id=detail.product_id,
            quantity=detail.quantity,
            subtotal=subtotal
        )
        db.add(db_detail)

    db_cart.totalprice = total_price
    db.commit()
    db.refresh(db_cart)

    return db_cart

@router.put("/{cart_id}", response_model=CartResponse)
def update_cart(cart_id: UUID, cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Map existing details
    existing_details = {detail.cartdetail_id: detail for detail in db_cart.details}
    updated_ids = set()

    total_price = 0

    for detail in cart.details:
        product = db.query(Product).filter(Product.product_id == detail.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {detail.product_id} not found")

        subtotal = product.price * detail.quantity

        if detail.cartdetail_id:  # update
            db_detail = existing_details.get(detail.cartdetail_id)
            if not db_detail:
                raise HTTPException(status_code=404, detail=f"CartDetail with ID {detail.cartdetail_id} not found")

            db_detail.product_id = detail.product_id
            db_detail.quantity = detail.quantity
            db_detail.subtotal = subtotal
            updated_ids.add(detail.cartdetail_id)
        else:  # new
            new_detail = CartDetail(
                cart_id=db_cart.cart_id,
                product_id=detail.product_id,
                quantity=detail.quantity,
                subtotal=subtotal
            )
            db.add(new_detail)

        total_price += subtotal

    # Xoá những CartDetail không còn tồn tại trong request
    for detail_id in existing_details:
        if detail_id not in updated_ids:
            db.query(CartDetail).filter(CartDetail.cartdetail_id == detail_id).delete()

    db_cart.totalprice = total_price
    db.commit()
    db.refresh(db_cart)

    return db_cart

@router.delete("/{cart_id}", response_model=CartResponse)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.query(CartDetail).filter(CartDetail.cart_id == cart_id).delete()
    db.delete(cart)
    db.commit()
    return {"message": f"Cart {cart_id} deleted successfully"}