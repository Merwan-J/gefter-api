from fastapi import APIRouter, Depends
from fastapi_injector import Injected
from api.core.dependencies import get_current_user
from api.invoices.models import (
    InvoiceCreate,
    InvoiceDetailRead,
    InvoiceRead,
)
from api.invoices.service import InvoiceService
from api.user.models import User


invoice_router = APIRouter(prefix="/invoices", tags=["invoices"])


@invoice_router.post("/")
async def create_invoice(
    invoice: InvoiceCreate,
    invoice_service: InvoiceService = Injected(InvoiceService),
    _: User = Depends(get_current_user),
):
    created_invoice = invoice_service.create_invoice(invoice)
    return InvoiceRead.model_validate(created_invoice)


@invoice_router.get("/")
async def get_invoices(
    invoice_service: InvoiceService = Injected(InvoiceService),
    user: User = Depends(get_current_user),
):
    return invoice_service.get_invoices(user.id)


@invoice_router.get("/{id}", response_model=InvoiceDetailRead)
async def get_invoice(
    id: str,
    invoice_service: InvoiceService = Injected(InvoiceService),
    user: User = Depends(get_current_user),
):
    return invoice_service.get_invoice_detail(id, user.id)
