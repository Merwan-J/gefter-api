from dataclasses import dataclass
from injector import inject
from fastapi import HTTPException

from api.invoice_shares.repository import InvoiceShareRepository
from api.invoice_shares.models import InvoiceShare


@inject
@dataclass
class InvoiceShareService:
    invoice_share_repository: InvoiceShareRepository

    def create_invoice_share(self) -> InvoiceShare:
        try:
            pass
        except Exception:
            raise HTTPException(
                status_code=500, detail="Unable to create invoice share"
            )
