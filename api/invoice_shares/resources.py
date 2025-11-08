from fastapi import APIRouter, Depends
from fastapi_injector import Injected
from typing import List
from uuid import UUID

from api.core.dependencies import get_current_user
from api.invoice_shares.models import InvoiceShareRead, InvoiceShareFilter
from api.invoice_shares.service import InvoiceShareService
from api.invoices.models import InvoiceDetailRead
from api.invoices.service import InvoiceService
from api.user.models import User


invoice_share_router = APIRouter(prefix="/invoice-shares", tags=["invoice_shares"])


@invoice_share_router.get("/", response_model=List[InvoiceShareRead])
async def get_invoice_shares(
    invoice_share_service: InvoiceShareService = Injected(InvoiceShareService),
    user: User = Depends(get_current_user),
    filter: InvoiceShareFilter | None = None,
):
    if filter == InvoiceShareFilter.I_OWE:
        invoice_shares = invoice_share_service.get_invoice_shares_by_debtor_id(user.id)
    elif filter == InvoiceShareFilter.OWED_TO_ME:
        invoice_shares = invoice_share_service.get_invoice_shares_by_creditor_id(user.id)
    else:
        invoice_shares = invoice_share_service.get_invoice_shares_by_user_id(user.id)

    return [InvoiceShareRead.model_validate(share) for share in invoice_shares]


@invoice_share_router.get("/{invoice_share_id}",  response_model=InvoiceShareRead)
async def get_invoice_share(
    invoice_share_id: UUID,
    invoice_service: InvoiceService = Injected(InvoiceService),
):
    invoice_share = invoice_service.get_invoice_detail(invoice_share_id)
    return InvoiceShareRead.model_validate(invoice_share)
    

@invoice_share_router.post("/{invoice_share_id}/pay", response_model=InvoiceDetailRead)
async def pay_invoice_share(
    invoice_share_id: UUID,
    invoice_share_service: InvoiceShareService = Injected(InvoiceShareService),
    invoice_service: InvoiceService = Injected(InvoiceService),
    _: User = Depends(get_current_user),
):
    share = invoice_share_service.get_invoice_share_by_id(invoice_share_id)
    return invoice_service.pay_invoice_share(share.invoice_id, invoice_share_id)


