from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductResponse, ProductCreate
from app.models.product_model import Product
from app.models.category_model import Category
from app.database import get_db
import logging
from uuid import UUID
import validators

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/", response_model=list[ProductResponse])
def get_All_Product(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Kiểm tra xem sản phẩm đã tồn tại hay chưa
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    # Kiểm tra xem category_id có tồn tại trong bảng category hay không
    category = db.query(Category).filter(Category.category_id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    # Kiểm tra xem imgproduct có phải là một URL hợp lệ hay không
    if product.imgproduct and not validators.url(product.imgproduct):
        raise HTTPException(status_code=400, detail="Invalid image URL")
    # Kiểm tra xem price có phải là một số dương hay không
    if not isinstance(product.price, (int, float)):
        raise HTTPException(status_code=400, detail="Price must be a number")
    if product.price < 0:
        raise HTTPException(status_code=400, detail="Price must be a positive number")
    try:
        new_product = Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, product: ProductResponse, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Chỉ cập nhật các trường được gửi trong JSON, bỏ qua createat và product_id
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key not in ["createdat", "product_id"]:
            setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}