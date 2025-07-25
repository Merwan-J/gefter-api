from dataclasses import dataclass
from uuid import UUID
from injector import inject

from api.core.repository import DatabaseEngineProvider
from api.invoices.models import Invoice, InvoiceCreate, InvoiceShare


@inject 
@dataclass 
class InvoiceRepository:
    engine_provider: DatabaseEngineProvider


    def create_invoice_with_shares(self, invoice_create: InvoiceCreate) -> Invoice:
        with self.engine_provider.get_session() as session:
            invoice = Invoice(**invoice_create.model_dump())
            session.add(invoice)
            
            invoice_shares = [
                InvoiceShare(**share.model_dump(), invoice_id=invoice.id)
                for share in invoice_create.invoice_shares
            ]
            session.add_all(invoice_shares)
            
            session.commit()
            session.refresh(invoice)
            return invoice

    def save(self, invoice: Invoice) -> Invoice:
        with self.engine_provider.get_session() as session:
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            return invoice
        