from fastapi import FastAPI
from app.routes.user_route import router as user_router
from app.routes.product_route import router as product_router
from app.routes.category_route import router as category_router
from app.routes.wishlist_route import router as wishlist_router
from app.routes.cart_route import router as cart_router
from app.routes.invoice_route import router as invoice_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

app.include_router(user_router)

app.include_router(product_router)

app.include_router(category_router)

app.include_router(wishlist_router)

app.include_router(cart_router)

app.include_router(invoice_router)