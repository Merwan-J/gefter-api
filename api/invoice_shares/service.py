from dataclasses import dataclass
from injector import inject
from fastapi import HTTPException
from uuid import UUID

from api.invoice_shares.repository import InvoiceShareRepository
from api.invoice_shares.models import InvoiceShare, InvoiceShareCreate
from api.invoices.models import Invoice


@inject 
@dataclass 
class InvoiceShareService:
    invoice_share_repository: InvoiceShareRepository

    def create_invoice_share(self) -> InvoiceShare:
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unable to create invoice share")

