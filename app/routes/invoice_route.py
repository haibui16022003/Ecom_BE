from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from uuid import UUID, uuid4
from app.models import Invoice, InvoiceDetail, Cart, CartDetail, Product
from app.schemas.invoice_schema import InvoiceResponse

router = APIRouter(prefix="/invoice", tags=["Invoice"])


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.post("/from-cart/{cart_id}", response_model=InvoiceResponse)
def create_invoice_from_cart(cart_id: UUID, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    if not cart.details:
        raise HTTPException(status_code=400, detail="Cart is empty")

    invoice_id = uuid4()
    invoice = Invoice(
        invoice_id=invoice_id,
        user_id=cart.user_id,
        totalprice=cart.totalprice,
        status="Pending"
    )
    db.add(invoice)

    for detail in cart.details:
        invoice_detail = InvoiceDetail(
            invoicedetail_id=uuid4(),
            invoice_id=invoice_id,
            product_id=detail.product_id,
            quantity=detail.quantity,
            subtotal=detail.subtotal
        )
        db.add(invoice_detail)

    db.commit()
    db.refresh(invoice)
    return invoice

@router.put("/{invoice_id}/status")
def update_invoice_status(invoice_id: UUID, status: str = Body(...), db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.status = status
    db.commit()
    db.refresh(invoice)

    return {"message": f"Invoice {invoice_id} status updated to '{status}' successfully"}


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.query(InvoiceDetail).filter(InvoiceDetail.invoice_id == invoice_id).delete()
    db.delete(invoice)
    db.commit()

    return {"message": f"Invoice {invoice_id} deleted successfully"}
