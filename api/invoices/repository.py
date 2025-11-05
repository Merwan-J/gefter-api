from dataclasses import dataclass
from typing import List
from uuid import UUID
from injector import inject
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlmodel import select, Session
from sqlalchemy.engine import Engine

from api.core.repository import DatabaseEngineProvider
from api.invoices.models import Invoice, InvoiceCreate, InvoiceShare
from api.core.exceptions import NotFoundError


@inject
@dataclass
class InvoiceRepository:
    engine_provider: DatabaseEngineProvider

    def __post_init__(self):
        self.engine: Engine = self.engine_provider.get_engine()

    def create_invoice_with_shares(self, invoice_create: InvoiceCreate) -> Invoice:
        with Session(self.engine) as session:
            invoice_data = invoice_create.model_dump(exclude={"invoice_shares"})
            invoice = Invoice(**invoice_data)
            session.add(invoice)
            session.flush()

            invoice_shares = [
                InvoiceShare(**share.model_dump(), invoice_id=invoice.id)
                for share in invoice_create.invoice_shares
            ]
            session.add_all(invoice_shares)
            session.commit()

            query = (
                select(Invoice)
                .options(
                    selectinload(Invoice.invoice_shares).selectinload(
                        InvoiceShare.debtor
                    )
                )
                .options(selectinload(Invoice.creator))
                .where(Invoice.id == invoice.id)
            )

            invoice = session.exec(query).one()
            _ = invoice.invoice_shares  # Access to trigger lazy load if needed
            return invoice

    def get_invoice_detail(self, invoice_id: UUID) -> Invoice:
        with Session(self.engine) as session:
            query = (
                select(Invoice)
                .options(
                    selectinload(Invoice.invoice_shares).selectinload(
                        InvoiceShare.debtor
                    )
                )
                .options(selectinload(Invoice.creator))
                .where(Invoice.id == invoice_id)
            )

            try:
                invoice = session.exec(query).one()
                return invoice
            except NoResultFound:
                raise NotFoundError("Invoice not found")

    def get_invoices(self, user_id: UUID) -> List[Invoice]:
        with Session(self.engine) as session:
            query = (
                select(Invoice)
                .options(
                    selectinload(Invoice.invoice_shares).selectinload(
                        InvoiceShare.debtor
                    )
                )
                .options(selectinload(Invoice.creator))
                .where(Invoice.creator_id == user_id)
            )
            return session.exec(query).all()
