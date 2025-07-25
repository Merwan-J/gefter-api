from fastapi import APIRouter, Depends
from fastapi_injector import Injected
from api.core.dependencies import get_current_user
from api.invoices.models import InvoiceCreate, InvoiceRead
from api.invoices.service import InvoiceService
from api.user.models import User


invoice_router = APIRouter(prefix="/invoices", tags=["invoices"])


@invoice_router.post("/")
async def create_invoice(
    invoice: InvoiceCreate,
    invoice_service: InvoiceService = Injected(InvoiceService),
    _: User = Depends(get_current_user),
):
    invoice = invoice_service.create_invoice(invoice)
    return InvoiceRead(**invoice.model_dump())


@invoice_router.get("/{id}", response_model=InvoiceRead)
async def get_invoice(
    id: str,
    invoice_service: InvoiceService = Injected(InvoiceService),
    _: User = Depends(get_current_user),
):
    pass
