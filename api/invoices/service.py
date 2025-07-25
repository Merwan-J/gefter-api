from dataclasses import dataclass
from fastapi import HTTPException
from injector import inject

from api.invoices.models import Invoice, InvoiceCreate
from api.invoices.repository import InvoiceRepository


@inject
@dataclass
class InvoiceService:
    invoice_repository: InvoiceRepository

    def create_invoice(self, invoice_create: InvoiceCreate) -> Invoice:  
        try:
            invoice = self.invoice_repository.create_invoice_with_shares(invoice_create)
            return invoice
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unable to create invoice")